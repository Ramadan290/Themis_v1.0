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

const explanationMap = {
  0: [
    "Attrition risk is very low — this employee is highly likely to remain in the organization.",
    "Strong retention indicators — no signs of turnover.",
    "The employee appears highly engaged and stable."
  ],
  1: [
    "Moderate risk — some signs of potential disengagement, but not alarming.",
    "Risk is manageable, though continued monitoring is advised.",
    "Neutral risk — no urgent concerns but potential shifts could happen."
  ],
  2: [
    "The employee shows signs of dissatisfaction — consider proactive HR support.",
    "High attrition risk — review feedback, workload, or recognition gaps.",
    "This user may be considering departure — HR engagement recommended."
  ],
  3: [
    "Critical attrition risk — urgent action is required to retain this employee.",
    "Very high risk of losing this employee — immediate intervention advised.",
    "Likely departure — initiate conversation or retention planning quickly."
  ]
};

function getRandomExplanation(riskClass) {
  const options = explanationMap[riskClass] || ["No explanation available."];
  return options[Math.floor(Math.random() * options.length)];
}

function predictAttrition() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/attrition/${userId}`, {
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
      const riskLevel = data.risk_level;
      const riskClass = data.risk_class;
      const explanation = getRandomExplanation(riskClass);

      document.getElementById("resultBox").style.display = "block";
      document.getElementById("predictionOutput").innerHTML = `
        <strong>Predicted Attrition Risk:</strong> ${riskLevel}<br/><br/>
        <em>${explanation}</em>
      `;

      const actionBox = document.getElementById("actionBox");
      actionBox.style.display = "block";
      actionBox.innerHTML = "";

      if (riskClass === 2 || riskClass === 3) {
        const msg = document.createElement("p");
        msg.innerText = "Do you want to assign support or intervene?";
        const btn = document.createElement("button");
        btn.innerText = "Initiate Retention Plan";
        btn.onclick = () => window.location.href = "../../hr_payroll/hr_payroll_fixed/hr_payroll_fixed.html"; // placeholder
        actionBox.appendChild(msg);
        actionBox.appendChild(btn);
      } else {
        const msg = document.createElement("p");
        msg.innerText = "No action needed, but would you like to send positive feedback?";
        const btn = document.createElement("button");
        btn.innerText = "Send Recognition";
        btn.onclick = () => window.location.href = "../../hr_payroll/hr_payroll_fixed/hr_payroll_fixed.html"; // placeholder
        actionBox.appendChild(msg);
        actionBox.appendChild(btn);
      }
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Prediction Failed", "Not enough data to predict.", "error");
    });
}


function viewAttritionHistory() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/attrition-risk/history/${userId}`, {
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
      list.innerHTML = ""; // Clear previous results

      history.forEach(item => {
        const li = document.createElement("li");
        const date = new Date(item.predicted_at).toLocaleString();
        li.textContent = `${item.risk_level} Risk (${date})`;
        list.appendChild(li);
      });

      document.getElementById("historyBox").style.display = "block";
    })
    .catch(err => {
      console.error(err);
      Swal.fire("No History", "No attrition risk history found for this user.", "info");
    });
}

