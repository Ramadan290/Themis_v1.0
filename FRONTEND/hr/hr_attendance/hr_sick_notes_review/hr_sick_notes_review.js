const token = localStorage.getItem("token");
const userCache = {};
const attendanceCache = {};

document.addEventListener("DOMContentLoaded", () => {
  fetchSickNotes();
});

async function getUsernameById(userId) {
  if (userCache[userId]) return userCache[userId];
  try {
    const res = await fetch(`http://127.0.0.1:8000/auth/users/by-id/${userId}`, {
      headers: { Authorization: token }
    });
    if (!res.ok) throw new Error(`User fetch failed (${res.status})`);
    const user = await res.json();
    userCache[userId] = user.username;
    return user.username;
  } catch (err) {
    console.error("Error fetching user:", err);
    return "Unknown";
  }
}

async function getUserIdFromAttendance(attendanceId) {
  if (attendanceCache[attendanceId]) return attendanceCache[attendanceId];
  try {
    const res = await fetch(`http://127.0.0.1:8000/attendance-history/by-id/${attendanceId}`, {
      headers: { Authorization: token }
    });
    if (!res.ok) throw new Error(`Attendance fetch failed (${res.status})`);
    const attendance = await res.json();
    const userId = attendance.user_id;
    attendanceCache[attendanceId] = userId;
    return userId;
  } catch (err) {
    console.error("Error fetching attendance:", err);
    return null;
  }
}

async function fetchSickNotes() {
  try {
    const res = await fetch("http://127.0.0.1:8000/sick-notes/all", {
      headers: { Authorization: token }
    });
    if (!res.ok) throw new Error("Failed to fetch sick notes");
    const notes = await res.json();
    renderSickNotes(notes);
    renderReviewedNotes(notes);
  } catch {
    document.getElementById("sickNotesBody").innerHTML = "<tr><td colspan='8'>Failed to load data.</td></tr>";
    document.getElementById("reviewedNotesBody").innerHTML = "<tr><td colspan='7'>Failed to load data.</td></tr>";
  }
}

async function renderSickNotes(notes) {
  const tbody = document.getElementById("sickNotesBody");
  tbody.innerHTML = "";

  const pendingNotes = notes.filter(n => n.status.toLowerCase() === "pending");
  if (!pendingNotes.length) {
    tbody.innerHTML = "<tr><td colspan='8'>No pending sick notes.</td></tr>";
    return;
  }

  for (const note of pendingNotes) {
    const tr = document.createElement("tr");
    let username = "Unknown";

    const userId = await getUserIdFromAttendance(note.attendance_id);
    if (userId) username = await getUsernameById(userId);

    const submitted = note.submitted_at ? note.submitted_at.split("T")[0] : "—";

    tr.innerHTML = `
      <td>${note.id}</td>
      <td>${username}</td>
      <td>${note.attendance_id}</td>
      <td>${note.reason}</td>
      <td>${note.status}</td>
      <td>${note.review_comments || "—"}</td>
      <td>${submitted}</td>
      <td>
        <select id="decision-${note.id}">
          <option value="">--Decision--</option>
          <option value="approved">Approve</option>
          <option value="rejected">Reject</option>
        </select>
        <input type="text" id="comment-${note.id}" placeholder="Add comment" />
        <button onclick="submitReview(${note.id})">Submit</button>
      </td>
    `;
    tbody.appendChild(tr);
  }
}

async function renderReviewedNotes(notes) {
  const tbody = document.getElementById("reviewedNotesBody");
  tbody.innerHTML = "";

  const reviewedNotes = notes.filter(n =>
    n.status.toLowerCase() === "approved" || n.status.toLowerCase() === "rejected"
  );

  if (!reviewedNotes.length) {
    tbody.innerHTML = "<tr><td colspan='7'>No reviewed sick notes yet.</td></tr>";
    return;
  }

  for (const note of reviewedNotes) {
    const tr = document.createElement("tr");
    let username = "Unknown";

    const userId = await getUserIdFromAttendance(note.attendance_id);
    if (userId) username = await getUsernameById(userId);

    const submitted = note.submitted_at ? note.submitted_at.split("T")[0] : "—";
    const status = note.status.charAt(0).toUpperCase() + note.status.slice(1);

    tr.innerHTML = `
      <td>${note.id}</td>
      <td>${username}</td>
      <td>${note.attendance_id}</td>
      <td>${note.reason}</td>
      <td>${status}</td>
      <td>${note.review_comments || "—"}</td>
      <td>${submitted}</td>
    `;
    tr.style.opacity = "0.5";
    tbody.appendChild(tr);
  }
}

async function submitReview(noteId) {
  const decision = document.getElementById(`decision-${noteId}`).value;
  const comment = document.getElementById(`comment-${noteId}`).value;

  if (!decision) {
    Swal.fire("Missing Input", "Please select a decision.", "warning");
    return;
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/sick-notes/review/${noteId}?decision=${decision}&comment=${encodeURIComponent(comment)}`, {
      method: "PUT",
      headers: { Authorization: token }
    });

    if (res.ok) {
      Swal.fire("Success", `Note ${decision}`, "success");
      fetchSickNotes();
    } else {
      const err = await res.json();
      Swal.fire("Error", err.detail || "Review failed", "error");
    }
  } catch {
    Swal.fire("Error", "Server error occurred", "error");
  }
}
