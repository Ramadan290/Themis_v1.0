document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  const attendanceRecordsElement = document.getElementById('attendance-records');
  const logAttendanceButton = document.getElementById('log-attendance-button');
  const sickNoteForm = document.getElementById('sick-note-form');
  const sickNoteMessage = document.getElementById('sick-note-message');
  const sickNoteFormSection = document.getElementById('sick-note-form-section');

  // Disable sick note form visually and functionally on load
  document.querySelectorAll('#sick-note-form input, #sick-note-form textarea, #sick-note-form button').forEach(el => {
    el.disabled = true;
  });
  sickNoteFormSection.classList.add('sick-note-disabled');

  // Log Attendance
  logAttendanceButton.addEventListener('click', async () => {
    if (logAttendanceButton.disabled) return;

    try {
      const response = await fetch('http://127.0.0.1:8000/attendance-sheet/log', {
        method: 'POST',
        headers: { 'Authorization': token },
      });

      if (response.ok) {
        const data = await response.json();
       Swal.fire(`Attendance logged successfully at ${data.logged_at}` , 'success');
        fetchAttendanceRecords();
        markButtonAsLogged();
      } else if (response.status === 400) {
        markButtonAsLogged();
      } else {
        Swal.fire('Failed to log attendance.' , 'failure');
      }
    } catch (error) {
      console.error('Error logging attendance:', error);
    }
  });

  const markButtonAsLogged = () => {
    logAttendanceButton.disabled = true;
    logAttendanceButton.innerText = 'Logged';
    logAttendanceButton.style.backgroundColor = '#bbb';
    logAttendanceButton.style.color = '#666';
    logAttendanceButton.style.cursor = 'not-allowed';
    logAttendanceButton.style.pointerEvents = 'none';
    logAttendanceButton.title = 'You already logged attendance today.';
  };

  const disableIfAlreadyLogged = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/attendance-history/my', {
        method: 'GET',
        headers: { 'Authorization': token }
      });

      if (!response.ok) return;
      const records = await response.json();
      const today = new Date().toLocaleDateString('en-CA');
      const alreadyLogged = records.find(r => r.status === 'present' && r.date === today);
      if (alreadyLogged) markButtonAsLogged();

    } catch (err) {
      console.error('Error checking attendance status:', err);
    }
  };

  const fetchAttendanceRecords = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/attendance-history/my', {
        method: 'GET',
        headers: { 'Authorization': token },
      });

      attendanceRecordsElement.innerHTML = '';

      if (!response.ok) {
        attendanceRecordsElement.innerHTML = '<tr><td colspan="4">No attendance records found.</td></tr>';
        return;
      }

      const records = await response.json();

      if (records.length === 0) {
        attendanceRecordsElement.innerHTML = '<tr><td colspan="4">No attendance records found.</td></tr>';
      }

      records.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${record.attendance_id || record.id}</td>
          <td>${record.date}</td>
          <td>${record.status || 'N/A'}</td>
          <td><a href="#">Apply</a></td>
        `;

        row.style.cursor = 'pointer';

        row.addEventListener('click', () => {
          const status = record.status?.toLowerCase();
          const id = record.attendance_id || record.id;

          if (status === 'absent' || status === 'late') {
            document.getElementById('attendance-id').value = id;
            document.querySelectorAll('#sick-note-form input, #sick-note-form textarea, #sick-note-form button').forEach(el => {
              el.disabled = false;
            });
            sickNoteFormSection.classList.remove('sick-note-disabled');
            sickNoteFormSection.classList.add('sick-note-enabled');
            showNotification("You can now submit a sick note for this entry.", "success");
          } else {
            document.getElementById('attendance-id').value = '';
            document.querySelectorAll('#sick-note-form input, #sick-note-form textarea, #sick-note-form button').forEach(el => {
              el.disabled = true;
            });
            sickNoteFormSection.classList.remove('sick-note-enabled');
            sickNoteFormSection.classList.add('sick-note-disabled');
            showNotification("Sick note only allowed for 'absent' or 'late' status.", "error");
          }
        });

        attendanceRecordsElement.appendChild(row);
      });

    } catch (error) {
      console.error('Error fetching attendance records:', error);
    }
  };

  sickNoteForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const attendanceId = document.getElementById('attendance-id').value;
    const reason = document.getElementById('reason').value;
    const fileInput = document.getElementById('sick-note-file');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('attendance_id', attendanceId);
    formData.append('reason', reason);
    if (file) formData.append('file', file, file.name);

    try {
      const response = await fetch('http://127.0.0.1:8000/sick-notes/submit', {
        method: 'POST',
        headers: { 'Authorization': token },
        body: formData
      });

      if (response.ok) {
        showNotification("Sick note submitted successfully", "success");
        sickNoteForm.reset();
        fetchMySickNotes();
        document.querySelectorAll('#sick-note-form input, #sick-note-form textarea, #sick-note-form button').forEach(el => {
          el.disabled = true;
        });
        sickNoteFormSection.classList.remove('sick-note-enabled');
        sickNoteFormSection.classList.add('sick-note-disabled');
      } else {
        showNotification("Failed to submit sick note", "error");
      }
    } catch (error) {
      console.error("Error submitting sick note:", error);
      showNotification("Error submitting sick note", "error");
    }
  });

  const fetchMySickNotes = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/sick-notes/user/${userId}`, {
        method: 'GET',
        headers: { 'Authorization': token }
      });

      const container = document.getElementById('sick-note-content');

      if (response.ok) {
        const data = await response.json();
        const notesArray = Array.isArray(data) ? data : [data];
        renderSickNotes(notesArray);
      } else {
        container.innerHTML = '<p>No sick notes found for this session.</p>';
      }
    } catch (error) {
      console.error('Error fetching sick notes:', error);
      document.getElementById('sick-note-content').innerHTML = '<p>Error loading sick notes.</p>';
    }
  };

  const renderSickNotes = (notes) => {
    const container = document.getElementById('sick-note-content');
    container.innerHTML = '';

    if (notes.length === 0) {
      container.innerHTML = '<p>No sick note found for this session.</p>';
      return;
    }

    notes.forEach(note => {
      const card = document.createElement('div');
      card.className = 'sick-note-entry';

      card.innerHTML = `
        <p><strong>Attendance ID:</strong> ${note.attendance_id}</p>
        <p><strong>Reason:</strong> ${note.reason}</p>
        <p><strong>Status:</strong> ${note.status}</p>
        <p><strong>Submitted At:</strong> ${new Date(note.submitted_at).toLocaleString()}</p>
        ${note.review_comments ? `<p><strong>Review:</strong> ${note.review_comments}</p>` : ''}
        ${note.file_name ? `<p><strong>File:</strong> <a href="/path/to/uploads/${note.file_name}" target="_blank">${note.file_name}</a></p>` : ''}
      `;

      container.appendChild(card);
    });
  };

  function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';
    notification.style.padding = '1rem 2rem';
    notification.style.borderRadius = '8px';
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.style.color = 'white';
    notification.style.fontWeight = 'bold';
    notification.style.zIndex = 9999;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 500);
    }, 3000);
  }

  setTimeout(() => {
    fetchMySickNotes();
    disableIfAlreadyLogged();
    fetchAttendanceRecords();
  }, 100);
});