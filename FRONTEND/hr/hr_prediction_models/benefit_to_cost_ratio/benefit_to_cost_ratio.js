document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  if (!token) {
    Swal.fire("Unauthorized", "Please log in again.", "warning");
    return;
  }

  fetch("http://127.0.0.1:8000/auth/all", {
    headers: {
      "Authorization": token,
      "Content-Type": "application/json"
    }
  })
    .then(res => res.json())
    .then(users => {
      const tbody = document.getElementById("userTableBody");
      users.forEach(user => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${user.id}</td>
          <td>${user.username}</td>
          <td>${user.role}</td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Failed to fetch users:", err);
      Swal.fire("Error", "Could not load users.", "error");
    });
});

const bcrSentences = {
  veryLow: [
    "This user provides significantly low return relative to their cost.",
    "The BCR score indicates the user may require restructuring or reassignment.",
    "Performance output is heavily outweighed by cost — action is recommended."
  ],
  low: [
    "Below-average value detected — some benefits may not justify the current cost.",
    "Moderate BCR — potential improvements needed to justify investment.",
    "This user may need focused upskilling to increase efficiency."
  ],
  high: [
    "This employee offers solid value — benefits clearly outweigh the cost.",
    "BCR indicates a valuable contributor — consider ongoing support.",
    "Strong return on investment detected — a reliable performer."
  ],
  veryHigh: [
    "Top-tier BCR — this employee is highly valuable to the organization.",
    "Excellent return on cost — ideal candidate for recognition or promotion.",
    "Exceptional value — critical asset worth investing in."
  ]
};

function getBCRCategory(score) {
  if (score <= 0.010) return "veryLow";
  if (score <= 0.019) return "low";
  if (score <= 0.022) return "high";
  return "veryHigh";
}

function getRandomSentence(category) {
  const options = bcrSentences[category] || ["No comment available."];
  return options[Math.floor(Math.random() * options.length)];
}

function predictBCR() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/bcr/${userId}`, {
    method: "POST",
    headers: {
      "Authorization": token,
      "Content-Type": "application/json"
    }
  })
    .then(res => {
      if (!res.ok) {
        throw new Error(`Error ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      const score = data.bcr_score.toFixed(3);
      const category = getBCRCategory(data.bcr_score);
      const sentence = getRandomSentence(category);

      document.getElementById("resultBox").style.display = "block";
      document.getElementById("predictionOutput").innerHTML = `
        <strong>BCR Score:</strong> ${score}<br/><br/>
        <em>${sentence}</em>
      `;

      const actionBox = document.getElementById("actionBox");
      actionBox.style.display = "block";
      actionBox.innerHTML = "";

      // Payroll button
      const payrollBtn = document.createElement("button");
      payrollBtn.innerText = "Go to Payroll";
      payrollBtn.onclick = () => window.location.href = "../../hr_payroll/hr_payroll_fixed/hr_payroll_fixed.html"; 
      actionBox.appendChild(payrollBtn);

      // Attendance button
      const attendanceBtn = document.createElement("button");
      attendanceBtn.innerText = "Check Attendance";
      attendanceBtn.style.marginLeft = "10px";
      attendanceBtn.onclick = () => window.location.href = "../../hr_attendance/hr_attendance_management/hr_attendance.html"; 
      actionBox.appendChild(attendanceBtn);
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Prediction Failed", "Could not predict BCR.", "error");
    });
}


function viewBCRHistory() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/bcr/history/${userId}`, {
    method: "GET",
    headers: {
      "Authorization": token,
      "Content-Type": "application/json"
    }
  })
    .then(res => {
      if (!res.ok) {
        throw new Error("History not found");
      }
      return res.json();
    })
    .then(history => {
      const list = document.getElementById("historyList");
      list.innerHTML = "";

      history.forEach(item => {
        const li = document.createElement("li");
        const date = new Date(item.predicted_at).toLocaleString();
        li.textContent = `BCR Score: ${item.bcr_score} (${date})`;
        list.appendChild(li);
      });

      document.getElementById("historyBox").style.display = "block";
    })
    .catch(err => {
      console.error(err);
      Swal.fire("No History", "No BCR history found for this user.", "info");
    });
}
