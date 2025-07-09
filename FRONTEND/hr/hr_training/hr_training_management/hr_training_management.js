document.addEventListener("DOMContentLoaded", () => {
  const baseURL = "http://127.0.0.1:8000";
  const headers = {
    "Authorization": localStorage.getItem("token"),
    "Content-Type": "application/json"
  };

  let courses = []; // Global list of courses

  function loadCourses() {
    fetch(`${baseURL}/skills/courses`, { headers })
      .then(res => res.json())
      .then(data => {
        courses = data;

        const tbody = document.querySelector("#courseTable tbody");
        tbody.innerHTML = "";

        const courseSelect = document.getElementById("trainingCourseName");
        courseSelect.innerHTML = `<option value="" disabled selected>Select a course</option>`;

        data.forEach(course => {
          tbody.innerHTML += `
            <tr>
              <td>${course.course_name}</td>
              <td>${course.skill_targeted}</td>
              <td>${course.difficulty_level}</td>
              <td>${course.cost}</td>
              <td>${course.duration_days}</td>
              <td><button class="delete" onclick="deleteCourse(${course.id})">Delete</button></td>
            </tr>`;

          courseSelect.innerHTML += `<option value="${course.course_name}">${course.course_name}</option>`;
        });
      });
  }

  document.getElementById("add-course-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const payload = {
      course_name: courseName.value,
      skill_targeted: skillTargeted.value,
      difficulty_level: Number(difficultyLevel.value),
      cost: Number(cost.value),
      duration_days: Number(duration.value)
    };
    fetch(`${baseURL}/skills/courses`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload)
    }).then(() => {
      e.target.reset();
      loadCourses();
    });
  });

  window.deleteCourse = function(id) {
    fetch(`${baseURL}/skills/courses/${id}`, {
      method: "DELETE",
      headers
    }).then(() => loadCourses());
  };

  // Assign training using username and course name
  document.getElementById("assign-training-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = assignUsername.value.trim();
    const courseName = trainingCourseName.value;

    try {
      // Get user ID by username
      const resUser = await fetch(`${baseURL}/auth/users/by-username/${username}`, { headers });
      if (!resUser.ok) throw new Error("User not found");
      const userData = await resUser.json();

      // Get course ID from selected course name
      const selectedCourse = courses.find(c => c.course_name === courseName);
      if (!selectedCourse) throw new Error("Course not found");

      const payload = {
        user_id: userData.id,
        training_course_id: selectedCourse.id
      };

      const res = await fetch(`${baseURL}/training/assign`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error("Assignment failed");

      Swal.fire("Success", "Training assigned!", "success");
      e.target.reset();
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Failed to assign training. Check username or course.", "error");
    }
  });

  document.getElementById("check-status-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = checkUsername.value.trim();

    try {
      const resUser = await fetch(`${baseURL}/auth/users/by-username/${username}`, { headers });
      if (!resUser.ok) throw new Error("User not found");
      const userData = await resUser.json();

      const resStatus = await fetch(`${baseURL}/training/status/${userData.id}`, { headers });
      if (!resStatus.ok) throw new Error("Training status fetch failed");

      const trainingData = await resStatus.json();
      const table = document.getElementById("userTrainingTable");
      const tbody = table.querySelector("tbody");
      tbody.innerHTML = "";

      trainingData.forEach(t => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${t.training_id}</td>
          <td>${(courses.find(c => c.id === t.training_course_id) || {}).course_name || "Unknown"}</td>
          <td>${t.completed ? "✅ Yes" : "❌ No"}</td>
          <td>${t.progress ?? "0"}%</td>
          <td>${t.score !== null ? t.score : "N/A"}</td>
          <td>${t.cost_of_training !== null ? t.cost_of_training : "N/A"}</td>
          <td><button class="delete" onclick="deleteUserTraining(${t.training_id})">Remove</button></td>
        `;
        tbody.appendChild(row);
      });

      table.classList.remove("hidden-table");
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Username not found or no training data.", "error");
    }
  });

  document.getElementById("hideResultsBtn").addEventListener("click", () => {
    document.getElementById("userTrainingTable").classList.add("hidden-table");
  });

  window.deleteUserTraining = function(id) {
    fetch(`${baseURL}/training/remove/${id}`, {
      method: "DELETE",
      headers
    }).then(() => {
      Swal.fire("Removed", "Training deleted.", "info");
      document.getElementById("check-status-form").dispatchEvent(new Event("submit"));
    });
  };

  loadCourses();
});
