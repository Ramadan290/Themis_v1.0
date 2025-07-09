document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  if (!token) {
    Swal.fire("Unauthorized", "Please log in again.", "warning");
    return;
  }

  fetch("http://127.0.0.1:8000/auth/with-department", {
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
          <td>${user.department}</td>

        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Failed to fetch users:", err);
      Swal.fire("Error", "Could not load users.", "error");
    });
});

function predictRoleFit() {
  const userId = document.getElementById("userIdInput").value.trim();
  const token = localStorage.getItem("token");

  if (!userId) {
    Swal.fire("Missing Input", "Please enter a User ID.", "info");
    return;
  }

  fetch(`http://127.0.0.1:8000/predict/role-fitting/${userId}`, {
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
      const fitScore = (data.fit_score * 100).toFixed(2);
      const decision = data.decision;
      const message = data.message;

      // Display result
      document.getElementById("resultBox").style.display = "block";
      document.getElementById("fitScore").innerText = `Fit Score: ${fitScore}%`;
      document.getElementById("decisionText").innerHTML = `<strong>Decision:</strong> ${decision}`;
      document.getElementById("messageText").innerHTML = `<em>${message}</em>`;

      const actionBox = document.getElementById("actionBox");
      actionBox.innerHTML = "";
      actionBox.style.display = "none";

      // Handle Training Recommendation
      if (decision.includes("Training")) {
        const msg = document.createElement("p");
        msg.innerText = "Would you like to assign training based on skill gaps?";

        const btn = document.createElement("button");
        btn.innerText = "Assign Training";
        btn.onclick = () => window.location.href = "../../hr_training/hr_training_entry.html";

        actionBox.style.display = "block";
        actionBox.appendChild(msg);
        actionBox.appendChild(btn);
      }

      // Handle Department Transfer
      else if (decision === "Suggest department transfer" && data.suggested_department) {
        const msg = document.createElement("p");
        msg.innerHTML = `Suggested Department: <strong id="suggested-department">${data.suggested_department}</strong>`;

        const transferBtn = document.createElement("button");
        transferBtn.innerText = "Transfer User";
        transferBtn.classList.add("delete");
        transferBtn.onclick = async () => {
          try {
            const transferRes = await fetch(`http://127.0.0.1:8000/predict/role-fitting/transfer/${userId}?new_department=${encodeURIComponent(data.suggested_department)}`, {
              method: "PUT",
              headers: {
                "Authorization": token
              }
            });

            if (transferRes.ok) {
              const result = await transferRes.json();
              Swal.fire("Success", result.message, "success").then(() => {
                document.getElementById("resultBox").style.display = "none";
              });
            } else {
              Swal.fire("Error", "Failed to transfer user.", "error");
            }
          } catch (error) {
            console.error("Transfer failed:", error);
            Swal.fire("Error", "Could not complete department transfer.", "error");
          }
        };

        actionBox.style.display = "block";
        actionBox.appendChild(msg);
        actionBox.appendChild(transferBtn);
      }
    })
    .catch(err => {
      console.error(err);
      Swal.fire("Prediction Failed", "Could not analyze role fit. (Missing data will be prefilled during simulation)", "error");
    });
}
