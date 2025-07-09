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

const sentimentLabels = [
  "Very Negative",
  "Negative",
  "Neutral",
  "Positive",
  "Very Positive"
];

const sentimentDescriptions = {
  0: [
    "Severe dissatisfaction detected — emotional indicators suggest burnout, discontent, or alienation.",
    "Employee exhibits a critically negative sentiment — immediate check-in is recommended.",
    "Red-level sentiment — possibly dealing with accumulated stress, frustration, or isolation."
  ],
  1: [
    "Below-average sentiment — signs of disengagement, low motivation, or subtle dissatisfaction.",
    "Negative outlook detected — feedback should be reviewed and addressed proactively.",
    "Mood indicators suggest growing concerns or unmet needs in the work environment."
  ],
  2: [
    "Neutral emotional state — neither overly positive nor concerning.",
    "Balanced sentiment detected — this employee may be consistent but emotionally uninvested.",
    "Flat emotional outlook — further engagement could shift them in a positive direction."
  ],
  3: [
    "Positive sentiment — a healthy emotional state with signs of collaboration and satisfaction.",
    "Good morale — the employee appears to be engaged, comfortable, and aligned.",
    "Emotionally motivated — working in sync with organizational goals."
  ],
  4: [
    "Very positive sentiment — high motivation, satisfaction, and psychological safety detected.",
    "Excellent outlook — ideal engagement level and well-being observed.",
    "This employee radiates positivity — likely a strong team contributor and culture driver."
  ]
};

function getRandomExplanation(score) {
  const list = sentimentDescriptions[score] || ["No explanation available."];
  return list[Math.floor(Math.random() * list.length)];
}

function getSentimentClass(score) {
  switch (score) {
    case 0: return "sentiment-bad";
    case 1: return "sentiment-low";
    case 2: return "sentiment-neutral";
    case 3: return "sentiment-good";
    case 4: return "sentiment-great";
    default: return "sentiment-neutral";
  }
}

function predictSentiment() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/sentiment_score/${userId}`, {
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
      const score = data.sentiment_score;
      const label = sentimentLabels[score];
      const explanation = getRandomExplanation(score);

      // Show result box
      document.getElementById("resultBox").style.display = "block";

      // Show sentiment with colored badge
      const labelEl = document.getElementById("sentimentLabel");
      labelEl.innerHTML = `Sentiment: <span class="sentiment-badge ${getSentimentClass(score)}">${label}</span>`;

      // Explanation
      document.getElementById("sentimentExplanation").innerHTML = `<em>${explanation}</em>`;

      // Action buttons
      const actionBox = document.getElementById("actionBox");
      actionBox.innerHTML = "";
      actionBox.style.display = "block";

      if (score >= 3) {
        const msg = document.createElement("p");
        msg.innerText = "Would you like to recognize or reward this employee?";
        const btn1 = document.createElement("button");
        btn1.innerText = "Give Positive Feedback";
        btn1.onclick = () => window.location.href = "../../hr_payroll/hr_adjustments/hr_adjustments.html";

        const btn2 = document.createElement("button");
        btn2.innerText = "Assign Bonus";
        btn2.style.marginLeft = "10px";
        btn2.onclick = () => window.location.href = "../../hr_payroll/hr_adjustments/hr_adjustments.html";

        actionBox.appendChild(msg);
        actionBox.appendChild(btn1);
        actionBox.appendChild(btn2);
      } else if (score <= 1) {
        const msg = document.createElement("p");
        msg.innerText = "Do you want to review their comments or offer support?";
        const btn1 = document.createElement("button");
        btn1.innerText = "Review Feedback";
        btn1.onclick = () => window.location.href = "../../hr_news/hr_news.html";

        const btn2 = document.createElement("button");
        btn2.innerText = "Open Support Case";
        btn2.style.marginLeft = "10px";
        btn2.classList.add("delete");
        btn2.onclick = () => window.location.href = "../../hr_training/hr_training_entry.html";

        actionBox.appendChild(msg);
        actionBox.appendChild(btn1);
        actionBox.appendChild(btn2);
      }
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Prediction Failed", "Could not analyze sentiment (Missing user data (will be prefilled in simulation)).", "error");
    });
}


function viewSentimentHistory() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/sentiment-score/history/${userId}`, {
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
        li.textContent = `Sentiment Score: ${item.sentiment_score} (${date})`;
        list.appendChild(li);
      });

      document.getElementById("historyBox").style.display = "block";
    })
    .catch(err => {
      console.error(err);
      Swal.fire("No History", "No sentiment score history found for this user.", "info");
    });
}
