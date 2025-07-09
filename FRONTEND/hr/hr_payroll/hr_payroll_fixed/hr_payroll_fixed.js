document.addEventListener("DOMContentLoaded", () => {
  let token = localStorage.getItem("token");

  // Ensure Bearer prefix
  if (token && !token.startsWith("Bearer ")) {
    token = `Bearer ${token}`;
    localStorage.setItem("token", token);
  }

  if (!token) {
    Swal.fire("Unauthorized", "Please log in to continue.", "warning");
    return;
  }

  const headers = {
    "Authorization": token,
    "Content-Type": "application/json"
  };

  // === 1. Fetch all fixed salaries ===
  fetch("http://127.0.0.1:8000/payroll-fixed/get/all", {
    method: "GET",
    headers: headers
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to fetch payroll list");
      return response.json();
    })
    .then(data => {
      const tableBody = document.getElementById("payroll-table-body");
      tableBody.innerHTML = "";
      data.forEach(entry => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${entry.user_id}</td>
          <td>${entry.user.username}</td>
          <td>${entry.user.role}</td>
          <td>${entry.base_salary}</td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Error", "Could not load fixed salary data.", "error");
    });

  // === 2. Generate fixed salaries ===
  window.generateFixedSalaries = () => {
    const defaultSalary = document.getElementById("defaultSalary").value;

    if (!defaultSalary) {
      Swal.fire("Missing Input", "Please enter a default salary.", "warning");
      return;
    }

    fetch("http://127.0.0.1:8000/payroll-fixed/generate", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ default_salary: parseFloat(defaultSalary) })
    })
      .then(res => res.json())
      .then(data => {
        Swal.fire("Success", data.message, "success").then(() => location.reload());
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", "Failed to generate fixed salaries.", "error");
      });
  };

  // === 3. Update fixed salary by user ID ===
  window.updateFixedSalary = () => {
    const userId = document.getElementById("updateUserId").value;
    const newSalary = document.getElementById("updateSalary").value;

    if (!userId || !newSalary) {
      Swal.fire("Missing Input", "Please enter both User ID and new salary.", "warning");
      return;
    }

    fetch(`http://127.0.0.1:8000/payroll-fixed/update/${userId}`, {
      method: "PUT",
      headers: headers,
      body: JSON.stringify({ base_salary: parseFloat(newSalary) })
    })
      .then(res => {
        if (!res.ok) throw new Error("Update failed");
        return res.json();
      })
      .then(data => {
        Swal.fire(
          "Success",
          `Salary for <strong>${data.user.username}</strong> (${data.user.role}) updated to <strong>${data.base_salary}</strong>.`,
          "success"
        ).then(() => location.reload());
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", err.message || "Failed to update salary.", "error");
      });
  };
});
