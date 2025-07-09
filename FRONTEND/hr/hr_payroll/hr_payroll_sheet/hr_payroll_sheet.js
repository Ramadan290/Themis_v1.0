document.addEventListener("DOMContentLoaded", () => {
  let token = localStorage.getItem("token");

  if (!token || !token.startsWith("Bearer ")) {
    Swal.fire("Unauthorized", "Please log in.", "warning");
    return;
  }

  const headers = {
    "Authorization": token,
    "Content-Type": "application/json"
  };

  // === Fetch all payroll records ===
  fetch("http://127.0.0.1:8000/payroll/sheet/all", {
    method: "GET",
    headers: headers
  })
    .then(res => res.json())
    .then(data => {
      const tableBody = document.getElementById("payroll-sheet-body");
      tableBody.innerHTML = "";

      data.forEach(entry => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${entry.user_id}</td>
          <td>${entry.user.username}</td>
          <td>${entry.user.role}</td>
          <td><input type="number" value="${entry.salary}" id="salary-${entry.id}" /></td>
          <td>
            <select id="status-${entry.id}">
              <option value="draft" ${entry.status === "draft" ? "selected" : ""}>draft</option>
              <option value="approved" ${entry.status === "approved" ? "selected" : ""}>approved</option>
            </select>
          </td>
          <td>${new Date(entry.created_at).toLocaleString()}</td>
          <td>${new Date(entry.last_updated).toLocaleString()}</td>
          <td><button onclick="updatePayroll(${entry.id})">Update</button></td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Error", "Failed to load payroll sheet.", "error");
    });

  // === Generate new payroll sheet ===
  window.generatePayrollSheet = () => {
    fetch("http://127.0.0.1:8000/payroll/sheet", {
      method: "POST",
      headers: headers
    })
      .then(res => res.json())
      .then(data => {
        Swal.fire("Success", data.message, "success").then(() => location.reload());
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", "Failed to generate payroll sheet.", "error");
      });
  };

  // === Update payroll record ===
  window.updatePayroll = (id) => {
    const salary = document.getElementById(`salary-${id}`).value;
    const status = document.getElementById(`status-${id}`).value;

    if (!salary || !status) {
      Swal.fire("Missing Fields", "Salary and status are required.", "warning");
      return;
    }

    fetch(`http://127.0.0.1:8000/payroll/sheet/update/${id}`, {
      method: "PUT",
      headers: headers,
      body: JSON.stringify({
        salary: parseFloat(salary),
        status: status
      })
    })
      .then(res => {
        if (!res.ok) throw new Error("Update failed");
        return res.json();
      })
      .then(data => {
        Swal.fire("Success", "Payroll updated.", "success").then(() => location.reload());
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", err.message || "Update failed.", "error");
      });
  };
});
