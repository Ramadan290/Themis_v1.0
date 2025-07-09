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

function mapScoreLabel(score) {
  switch (score) {
    case 0: return "Low";
    case 1: return "Rational";
    case 2: return "Good";
    case 3: return "Excellent";
    default: return "Unknown";
  }
}

const explanationSentences = {
  0: [
    "The performance level is currently low, indicating the need for immediate support and improvement.",
    "This employee may be struggling and could benefit from additional training or mentoring.",
    "Low performance detected — proactive steps are recommended to address potential issues."
  ],
  1: [
    "This is a rational performance level — stable but with room for enhancement.",
    "Performance is within acceptable range, showing consistency but not exceeding expectations.",
    "A rational performance tier — dependable but not yet exemplary."
  ],
  2: [
    "Good performance achieved — demonstrating consistent and commendable results.",
    "This employee is performing well and meeting expectations reliably.",
    "A strong contributor showing regular effectiveness and output quality."
  ],
  3: [
    "An excellent performer — demonstrating exceptional quality and consistency.",
    "Outstanding performance level — exceeding expectations across the board.",
    "This employee stands out with top-tier efficiency and impact."
  ]
};

function getRandomExplanation(score) {
  const options = explanationSentences[score] || ["No explanation available."];
  return options[Math.floor(Math.random() * options.length)];
}

function predictPerformance() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/performance/${userId}`, {
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
      const score = data.performance_score;
      const label = mapScoreLabel(score);
      const explanation = getRandomExplanation(score);

      document.getElementById("resultBox").style.display = "block";
      document.getElementById("predictionOutput").innerHTML = `
        <strong>Predicted Performance Score:</strong> ${label}<br/><br/>
        <em>${explanation}</em>
      `;

      const actionBox = document.getElementById("actionBox");
      actionBox.style.display = "block";
      actionBox.innerHTML = "";

      if (score === 2 || score === 3) {
        const msg = document.createElement("p");
        msg.innerText = "Would you like to add any incentives?";
        const btn = document.createElement("button");
        btn.innerText = "Add Incentive";
        btn.onclick = () => window.location.href = "../../hr_payroll/hr_adjustments/hr_adjustments.html"; // redirection 
        actionBox.appendChild(msg);
        actionBox.appendChild(btn);
      } else if (score === 0 || score === 1) {
        const msg = document.createElement("p");
        msg.innerText = "Do you want to penalize this user?";
        const btn = document.createElement("button");
        btn.innerText = "Penalize User";
        btn.classList.add("delete");
        btn.onclick = () => window.location.href = "../../hr_payroll/hr_adjustments/hr_adjustments.html"; // Update this
        actionBox.appendChild(msg);
        actionBox.appendChild(btn);
      }
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Prediction Failed", "Could not predict performance.", "error");
    });
}


function viewPerformanceHistory() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/performance/history/${userId}`, {
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
        const label = mapScoreLabel(item.performance_score);
        li.textContent = `${label} (${date})`;
        list.appendChild(li);
      });

      document.getElementById("historyBox").style.display = "block";
    })
    .catch(err => {
      console.error(err);
      Swal.fire("No History", "No prediction history found for this user.", "info");
    });
}
