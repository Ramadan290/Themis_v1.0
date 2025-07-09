document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  if (!token || !token.startsWith("Bearer ")) {
    Swal.fire("Unauthorized", "Please log in.", "warning");
    return;
  }

  const headers = {
    Authorization: token,
    "Content-Type": "application/json"
  };

  // === Add Benefit to Catalog ===
  window.addBenefitToCatalog = () => {
    const name = document.getElementById("benefitName").value.trim();
    const description = document.getElementById("benefitDesc").value.trim();
    const amount = document.getElementById("benefitAmount").value;

    if (!name || !description || !amount) {
      Swal.fire("Missing Fields", "All fields are required.", "warning");
      return;
    }

    fetch("http://127.0.0.1:8000/catalog/benefit/add", {
      method: "POST",
      headers,
      body: JSON.stringify({ name, description, default_amount: parseFloat(amount) })
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to add benefit");
        return res.json();
      })
      .then(() => {
        Swal.fire("Success", "Benefit added to catalog.", "success").then(() => location.reload());
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", "Could not add benefit.", "error");
      });
  };

  // === Fetch Benefit Catalog ===
  fetch("http://127.0.0.1:8000/catalog/benefit/list", {
    method: "GET",
    headers
  })
    .then(res => res.json())
    .then(data => {
      const tbody = document.getElementById("catalogTableBody");
      tbody.innerHTML = "";

      data.forEach(benefit => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${benefit.id}</td>
          <td>${benefit.name}</td>
          <td>${benefit.description}</td>
          <td>${benefit.default_amount}</td>
          <td><button onclick="deleteBenefit(${benefit.id})">Delete</button></td>
        `;
        tbody.appendChild(row);
      });
    });

  // === Delete Benefit ===
  window.deleteBenefit = (id) => {
    fetch(`http://127.0.0.1:8000/catalog/benefit/${id}`, {
      method: "DELETE",
      headers
    })
      .then(res => {
        if (!res.ok) throw new Error("Delete failed");
        return res.text();
      })
      .then(() => {
        Swal.fire("Deleted", "Benefit removed from catalog.", "success").then(() => location.reload());
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", "Could not delete benefit.", "error");
      });
  };

  // === Assign Benefit to User ===
  window.assignBenefitToUser = () => {
    const username = document.getElementById("assignUsername").value.trim();
    const benefitId = document.getElementById("assignBenefitId").value;

    if (!username || !benefitId) {
      Swal.fire("Missing Fields", "Username and Benefit ID are required.", "warning");
      return;
    }

    fetch(`http://127.0.0.1:8000/auth/users/by-username/${username}`, {
      method: "GET",
      headers
    })
      .then(res => {
        if (!res.ok) throw new Error("User not found");
        return res.json();
      })
      .then(user => {
        return fetch("http://127.0.0.1:8000/benefit/assign", {
          method: "POST",
          headers,
          body: JSON.stringify({
            user_id: user.id,
            benefit_catalog_id: parseInt(benefitId)
          })
        });
      })
      .then(res => {
        if (!res.ok) throw new Error("Assignment failed");
        return res.json();
      })
      .then(() => {
        Swal.fire("Success", "Benefit assigned to user.", "success");
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", err.message || "Could not assign benefit.", "error");
      });
  };

  // === Fetch Benefits by Username ===
  window.fetchUserBenefits = () => {
    const username = document.getElementById("fetchUsername").value.trim();

    if (!username) {
      Swal.fire("Missing Username", "Please enter a username.", "warning");
      return;
    }

    fetch(`http://127.0.0.1:8000/auth/users/by-username/${username}`, {
      method: "GET",
      headers
    })
      .then(res => {
        if (!res.ok) throw new Error("User not found");
        return res.json();
      })
      .then(user => {
        return fetch(`http://127.0.0.1:8000/benefit/user/${user.id}`, {
          method: "GET",
          headers
        });
      })
      .then(res => {
        if (!res.ok) throw new Error("Fetch failed");
        return res.json();
      })
      .then(benefits => {
        const tbody = document.getElementById("userBenefitsTableBody");
        tbody.innerHTML = "";

        benefits.forEach(b => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${b.id}</td>
            <td>${b.benefit_catalog_id}</td>
            <td>${b.amount}</td>
          `;
          tbody.appendChild(row);
        });
      })
      .catch(err => {
        console.error(err);
        Swal.fire("Error", err.message || "Could not fetch benefits.", "error");
      });
  };
});
