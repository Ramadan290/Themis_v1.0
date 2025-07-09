document.addEventListener("DOMContentLoaded", () => {
  const baseURL = "http://127.0.0.1:8000";
  const headers = {
    "Authorization": localStorage.getItem("token"),
    "Content-Type": "application/json"
  };

  const form = document.getElementById("user-skill-form");
  const table = document.getElementById("userSkillTable");
  const tbody = table.querySelector("tbody");
  const hideBtn = document.getElementById("hideSkillsBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("skillUsername").value.trim();

    try {
      // Step 1: Get user by username
      const resUser = await fetch(`${baseURL}/auth/users/by-username/${username}`, { headers });
      if (!resUser.ok) throw new Error("User not found");
      const userData = await resUser.json();
      const userId = userData.id;

      // Step 2: Get user skills
      const resSkills = await fetch(`${baseURL}/skills/user-skills/${userId}`, { headers });
      if (!resSkills.ok) throw new Error("Skill data not found");
      const skillList = await resSkills.json();

      // Step 3: Populate table
      tbody.innerHTML = "";
      skillList.forEach(skill => {
        tbody.innerHTML += `
          <tr>
            <td>${skill.skill_name}</td>
            <td>${skill.skill_level ?? "N/A"}</td>
          </tr>
        `;
      });

      table.classList.remove("hidden-table");

    } catch (err) {
      Swal.fire("Error", err.message, "error");
    }
  });

  // Hide results
  hideBtn.addEventListener("click", () => {
    table.classList.add("hidden-table");
  });
});
