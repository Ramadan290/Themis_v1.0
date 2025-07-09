    document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    const userId = localStorage.getItem("user_id");

    if (!token || !userId) {
        Swal.fire("Missing Data", "User not logged in. Please log in again.", "warning");
        return;
    }

    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

 // === Fetch Skills ===
  fetch(`http://127.0.0.1:8000/skills/user-skills/${userId}`, { headers })
    .then(res => res.json())
    .then(data => {
      const skillsList = document.getElementById("skills-list");
      skillsList.innerHTML = "";

      if (data.length === 0) {
        skillsList.innerHTML = '<p class="empty-message">No skills assigned.</p>';
        return;
      }

      data.forEach(skill => {
        const card = document.createElement("div");
        card.classList.add("info-card");
        card.innerHTML = `
          <div>
            <span class="label">${skill.skill_name}</span>
            <p>Level: ${skill.skill_level}</p>
          </div>
        `;
        skillsList.appendChild(card);
      });
    })
    .catch(err => {
      document.getElementById("skills-list").innerHTML = `<p class="empty-message">Failed to load skills.</p>`;
      console.error("Skill fetch error:", err);
    });

      // === Fetch Trainings ===
  fetch(`http://127.0.0.1:8000/training/status/${userId}`, { headers })
    .then(res => res.json())
    .then(data => {
      const trainingList = document.getElementById("training-list");
      trainingList.innerHTML = "";

      if (!data || data.length === 0) {
        trainingList.innerHTML = '<p class="empty-message">No trainings assigned.</p>';
        return;
      }

      data.forEach(training => {
        const card = document.createElement("div");
        card.classList.add("info-card");

        card.innerHTML = `
          <div>
            <span class="label">Training ID: ${training.training_id}</span>
            <p>Course ID: ${training.training_course_id}</p>
            <p>Completed: ${training.completed ? "Yes ✅" : "No ❌"}</p>
            <p>Progress: ${training.progress}%</p>
            <p>Score: ${training.score}</p>
            <p>Cost: ${training.cost_of_training} EGP</p>
          </div>
        `;
        trainingList.appendChild(card);
      });
    })
    .catch(err => {
      document.getElementById("training-list").innerHTML = `<p class="empty-message">Failed to load trainings.</p>`;
      console.error("Training fetch error:", err);
    });
    });
