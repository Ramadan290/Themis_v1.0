const token = localStorage.getItem("token");
const userId = localStorage.getItem("user_id");

document.addEventListener("DOMContentLoaded", () => {
  fetch(`http://127.0.0.1:8000/status/${userId}`, {
    method: "GET",
    headers: {
      "Authorization": "Bearer " + token
    }
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("name").textContent = data.name || "N/A";
    document.getElementById("department").textContent = data.department || "N/A";
    document.getElementById("status").textContent = data.status || "N/A";
    document.getElementById("marital_status").textContent = data.personal?.marital_status || "N/A";

    document.getElementById("completion_rate").textContent = (data.task_completion_rate * 100).toFixed(1);

    document.getElementById("days_present").textContent = data.attendance.present ?? 0;
    document.getElementById("days_absent").textContent = data.attendance.absent ?? 0;
    document.getElementById("days_late").textContent = data.attendance.late ?? 0;

    document.getElementById("salary").textContent = data.payroll.salary ?? 0;
    document.getElementById("total_appraisals").textContent = data.payroll.total_appraisals ?? 0;
    document.getElementById("total_penalties").textContent = data.payroll.total_penalties ?? 0;
  })
  .catch(error => console.error("Error fetching employee status:", error));
});
