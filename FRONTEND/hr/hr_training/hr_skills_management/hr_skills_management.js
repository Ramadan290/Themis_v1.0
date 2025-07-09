document.addEventListener("DOMContentLoaded", () => {
  const baseURL = "http://127.0.0.1:8000";
  const headers = {
    "Authorization": localStorage.getItem("token"),
    "Content-Type": "application/json"
  };

  const skillTable = document.querySelector("#skillTable tbody");

  // Load all skills
  function loadSkills() {
    fetch(`${baseURL}/departments/skills/all`, { headers })
      .then(res => res.json())
      .then(data => {
        skillTable.innerHTML = "";
        data.forEach(skill => {
          skillTable.innerHTML += `
            <tr>
              <td>${skill.id}</td>
              <td>${skill.name}</td>
              <td>${skill.cost_of_training !== null ? skill.cost_of_training : "N/A"}</td>
              <td><button class="delete" onclick="deleteSkill(${skill.id})">Delete</button></td>
            </tr>
          `;
        });
      });
  }

  // Add new skill
  document.getElementById("add-skill-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("skillName").value.trim();
    const costValue = document.getElementById("skillCost").value;
    const cost = costValue === "" ? null : parseFloat(costValue);

    const payload = {
      skill_name: name,
      cost: cost
    };

    fetch(`${baseURL}/departments/skills/add`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload)
    }).then(res => {
      if (res.ok) {
        Swal.fire("Success", "Skill added.", "success");
        e.target.reset();
        loadSkills();
      } else {
        Swal.fire("Error", "Skill already exists or invalid data.", "error");
      }
    });
  });

  // Delete skill
  window.deleteSkill = function(id) {
    fetch(`${baseURL}/departments/skills/remove/${id}`, {
      method: "DELETE",
      headers
    }).then(res => {
      if (res.ok) {
        Swal.fire("Deleted", "Skill removed.", "info");
        loadSkills();
      } else {
        Swal.fire("Error", "Could not delete skill.", "error");
      }
    });
  };

  loadSkills();
});
