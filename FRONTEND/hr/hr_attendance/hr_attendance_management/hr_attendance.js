const token = localStorage.getItem("token");
let allLiveRecords = [];
let allHistoryRecords = [];
const userCache = {};

document.addEventListener("DOMContentLoaded", () => {
  fetchLiveAttendanceSheet();
  fetchAttendanceHistory();
});

function toggleSection(tableId, btn) {
  const section = document.getElementById(tableId);
  section.classList.toggle("hidden-table");

  if (section.classList.contains("hidden-table")) {
    btn.textContent = tableId.includes("History") ? "Show History" : "Show Sheet";
  } else {
    btn.textContent = tableId.includes("History") ? "Hide History" : "Hide Sheet";
  }
}

async function getUsernameById(userId) {
  if (userCache[userId]) return userCache[userId];
  try {
    const res = await fetch(`http://127.0.0.1:8000/auth/users/by-id/${userId}`, {
      headers: { Authorization: token }
    });
    if (!res.ok) throw new Error();
    const user = await res.json();
    userCache[userId] = user.username;
    return user.username;
  } catch {
    return "Unknown";
  }
}

// === LIVE SHEET ===

async function fetchLiveAttendanceSheet() {
  try {
    const res = await fetch("http://127.0.0.1:8000/attendance-sheet/all", {
      headers: { Authorization: token }
    });
    if (!res.ok) throw new Error();
    allLiveRecords = await res.json();
    renderLiveAttendanceTable(allLiveRecords);
  } catch {
    document.getElementById("liveAttendanceBody").innerHTML = `<tr><td colspan="5">Failed to load data.</td></tr>`;
  }
}

async function renderLiveAttendanceTable(records) {
  const tbody = document.getElementById("liveAttendanceBody");
  tbody.innerHTML = "";
  if (!records.length) {
    tbody.innerHTML = "<tr><td colspan='5'>No records found.</td></tr>";
    return;
  }

  for (const r of records) {
    const tr = document.createElement("tr");
    const username = await getUsernameById(r.user_id);
    const date = r.attendance_date?.split("T")[0] || "—";
    const session = r.session_tag || "—";
    const status = r.status || "None";

    tr.innerHTML = `
      <td>${r.id}</td>
      <td>${username}</td>
      <td>${date}</td>
      <td>${session}</td>
      <td>${status}</td>
    `;
    tbody.appendChild(tr);
  }
}

function filterLiveAttendance() {
  const usernameInput = document.getElementById("filter-live-username").value.toLowerCase();
  const from = document.getElementById("filter-live-from").value;
  const to = document.getElementById("filter-live-to").value;
  const statusFilter = document.querySelector('input[name="live-status"]:checked').value;

  const filtered = allLiveRecords.filter(r => {
    const uname = userCache[r.user_id]?.toLowerCase() || "";
    const recordDate = r.attendance_date?.split("T")[0] || "";
    const recordStatus = (r.status || "none").toLowerCase();

    const matchUser = uname.includes(usernameInput);
    const matchStatus = statusFilter === "" || recordStatus === statusFilter;
    const matchFrom = !from || recordDate >= from;
    const matchTo = !to || recordDate <= to;

    return matchUser && matchStatus && matchFrom && matchTo;
  });

  renderLiveAttendanceTable(filtered);
}

// === HISTORY ===

async function fetchAttendanceHistory() {
  try {
    const res = await fetch("http://127.0.0.1:8000/attendance-history/all", {
      headers: { Authorization: token }
    });
    if (!res.ok) throw new Error();
    allHistoryRecords = await res.json();
    renderHistoryTable(allHistoryRecords);
  } catch {
    document.getElementById("historyAttendanceBody").innerHTML = `<tr><td colspan="5">Failed to load history.</td></tr>`;
  }
}

async function renderHistoryTable(records) {
  const tbody = document.getElementById("historyAttendanceBody");
  tbody.innerHTML = "";
  if (!records.length) {
    tbody.innerHTML = "<tr><td colspan='5'>No history records.</td></tr>";
    return;
  }

  for (const r of records) {
    const tr = document.createElement("tr");
    const username = await getUsernameById(r.user_id);
    const date = r.date || "—";
    const status = r.status || "None";
    const created = r.created_at?.split("T")[0] || "—";

    tr.innerHTML = `
      <td>${r.attendance_id}</td>
      <td>${username}</td>
      <td>${date}</td>
      <td>${status}</td>
      <td>${created}</td>
    `;
    tbody.appendChild(tr);
  }
}

function filterHistoryAttendance() {
  const usernameInput = document.getElementById("filter-history-username").value.toLowerCase();
  const from = document.getElementById("filter-history-from").value;
  const to = document.getElementById("filter-history-to").value;
  const statusFilter = document.querySelector('input[name="history-status"]:checked').value;

  const filtered = allHistoryRecords.filter(r => {
    const uname = userCache[r.user_id]?.toLowerCase() || "";
    const recordDate = r.date || "";
    const recordStatus = (r.status || "none").toLowerCase();

    const matchUser = uname.includes(usernameInput);
    const matchStatus = statusFilter === "" || recordStatus === statusFilter;
    const matchFrom = !from || recordDate >= from;
    const matchTo = !to || recordDate <= to;

    return matchUser && matchStatus && matchFrom && matchTo;
  });

  renderHistoryTable(filtered);
}
