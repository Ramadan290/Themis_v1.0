document.addEventListener('DOMContentLoaded', () => {
  let token = localStorage.getItem('token');
  let userId = localStorage.getItem('user_id');

  if (!userId && token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      userId = payload.id;
      localStorage.setItem('user_id', userId);
      localStorage.setItem('role', payload.role);
    } catch (err) {
      console.error("Failed to decode token:", err);
    }
  }

  if (!token || !userId) {
    Swal.fire("Missing Data", "User is not logged in. Please log in again.", "warning");
    return;
  }

  const headers = {
    'Authorization': token,
    'Content-Type': 'application/json'
  };

  // === FIXED SALARY ===
  fetch(`http://127.0.0.1:8000/payroll-fixed/get/${userId}`, { headers })
    .then(res => res.json())
    .then(data => {
      document.getElementById('fixed-salary').textContent = `${data.base_salary} EGP`;
    })
    .catch(() => {
      document.getElementById('fixed-salary').textContent = 'Unavailable';
    });

  // === BENEFITS ===
  fetch(`http://127.0.0.1:8000/benefit/user/${userId}`, { headers })
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('benefits');
      container.innerHTML = '';
      if (Array.isArray(data) && data.length > 0) {
        data.forEach(item => {
          container.innerHTML += `
            <div class="info-card">
              <span class="label">Benefit:</span> ${item.amount} EGP
            </div>`;
        });
      } else {
        container.innerHTML = `<p class="empty-message">No benefits found.</p>`;
      }
    });

  // === APPRAISALS ===
  fetch(`http://127.0.0.1:8000/appraisals/user/${userId}`, { headers })
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('appraisals');
      container.innerHTML = '';
      if (Array.isArray(data) && data.length > 0) {
        data.forEach(item => {
          container.innerHTML += `
            <div class="info-card">
              <span class="label">Appraisal:</span> ${item.amount} EGP on ${new Date(item.appraisal_date).toLocaleDateString()}
            </div>`;
        });
      } else {
        container.innerHTML = `<p class="empty-message">No appraisals found.</p>`;
      }
    });

  // === PENALTIES ===
  fetch(`http://127.0.0.1:8000/penalties/user/${userId}`, { headers })
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('penalties');
      container.innerHTML = '';
      if (Array.isArray(data) && data.length > 0) {
        data.forEach(item => {
          container.innerHTML += `
            <div class="info-card">
              <span class="label">Penalty:</span> ${item.amount} EGP – ${item.reason}
            </div>`;
        });
      } else {
        container.innerHTML = `<p class="empty-message">No penalties found.</p>`;
      }
    });

  // === RAISE REQUEST SUBMIT ===
  document.getElementById('raise-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const amount = parseFloat(document.getElementById('requested-amount').value);
    const reason = document.getElementById('reason').value;

    if (!userId) {
      Swal.fire('Error', 'User ID not available.', 'error');
      return;
    }

    const response = await fetch(`http://127.0.0.1:8000/raise/submit`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        user_id: parseInt(userId),
        requested_amount: amount,
        reason: reason
      })
    });

    const result = await response.json();
    if (response.ok) {
      Swal.fire('Request Sent', `Request ID: ${result.request_uid}`, 'success');
      document.getElementById('raise-form').reset();
      fetchRaiseHistory();
    } else {
      Swal.fire('Error', result?.detail || 'Submission failed.', 'error');
    }
  });

  // === FETCH RAISE REQUEST HISTORY ===
  async function fetchRaiseHistory() {
    const response = await fetch(`http://127.0.0.1:8000/raise/user/${userId}`, {
      headers
    });

    const data = await response.json();
    const table = document.getElementById('raise-requests');
    table.innerHTML = '';

    data.forEach(req => {
      const row = `
        <tr>
          <td>${req.request_uid}</td>
          <td>${req.requested_amount}</td>
          <td>${req.reason}</td>
          <td>${req.status}</td>
          <td>${new Date(req.requested_at).toLocaleString()}</td>
        </tr>`;
      table.innerHTML += row;
    });
  }

  // Initial fetch of raise history
  fetchRaiseHistory();
});
