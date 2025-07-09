document.addEventListener("DOMContentLoaded", () => {
  let token = localStorage.getItem("token");

  if (!token || !token.startsWith("Bearer ")) {
    Swal.fire("Unauthorized", "Please log in to continue.", "warning");
    return;
  }

  const headers = {
    "Authorization": token,
    "Content-Type": "application/json"
  };

  let userId = null;
  let role = null;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    userId = payload.id;
    role = payload.role;
  } catch (err) {
    console.error("Invalid token:", err);
    Swal.fire("Error", "Invalid session. Please log in again.", "error");
    return;
  }

  // Hide filter for employee
  if (role === "employee") {
    document.getElementById("filter-section").style.display = "none";
  }

  // === Load default history based on role ===
  window.loadDefaultHistory = () => {
    const endpoint =
      role === "admin" || role === "hr"
        ? "http://127.0.0.1:8000/payroll-history/all"
        : `http://127.0.0.1:8000/payroll-history/user/${userId}`;

    fetch(endpoint, {
      method: "GET",
      headers: headers
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch payroll history");
        return res.json();
      })
      .then(data => renderHistoryTable(data))
      .catch(err => {
        console.error(err);
        Swal.fire("Error", "Could not load payroll history.", "error");
      });
  };

  // === Search by username (HR/Admin only) ===
  window.fetchHistoryByUsername = () => {
    const username = document.getElementById("filterUsername").value.trim();

    if (!username) {
      Swal.fire("Missing Input", "Please enter a username.", "warning");
      return;
    }

    fetch(`http://127.0.0.1:8000/auth/users/by-username/${username}`, {
      method: "GET",
      headers: headers
    })
      .then(res => {
        if (!res.ok) throw new Error("User not found");
        return res.json();
      })
      .then(user => {
        return fetch(`http://127.0.0.1:8000/payroll-history/user/${user.id}`, {
          method: "GET",
          headers: headers
        });
      })
      .then(res => {
        if (!res.ok) throw new Error("Payroll history not found for this user");
        return res.json();
      })
      .then(data => renderHistoryTable(data))
      .catch(err => {
        console.error(err);
        Swal.fire("Error", err.message || "Failed to load user history", "error");
      });
  };

  // === Render history table
  function renderHistoryTable(data) {
    const tableBody = document.getElementById("history-table-body");
    tableBody.innerHTML = "";

    if (!data.length) {
      const row = document.createElement("tr");
      row.innerHTML = `<td colspan="7" style="text-align:center;">No history records found.</td>`;
      tableBody.appendChild(row);
      return;
    }

    data.forEach(entry => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${entry.user_id}</td>
        <td>${entry.user?.username || "-"}</td>
        <td>${entry.user?.role || "-"}</td>
        <td>${entry.period}</td>
        <td>${entry.final_salary}</td>
        <td>${entry.status}</td>
        <td>${new Date(entry.recorded_at).toLocaleString()}</td>
      `;
      tableBody.appendChild(row);
    });
  }

  // Load default data on startup
  loadDefaultHistory();
});
