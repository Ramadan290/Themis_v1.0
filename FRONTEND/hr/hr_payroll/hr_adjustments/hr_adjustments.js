const BASE_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");

const headers = {
  "Authorization": token,
  "Content-Type": "application/json"
};

// === Utility: Get User ID by Username ===
async function getUserIdByUsername(username) {
  const res = await fetch(`${BASE_URL}/auth/users/by-username/${username}`, { headers });

  if (!res.ok) throw new Error("User not found");

  const data = await res.json();
  return data.id;
}

// === Utility: Get Dynamic Payroll ID from Username via user_id ===
async function getPayrollIdByUsername(username) {
  const userRes = await fetch(`${BASE_URL}/auth/users/by-username/${username}`, { headers });
  if (!userRes.ok) throw new Error("User not found");

  const user = await userRes.json();
  const userId = user.id;

  const payrollRes = await fetch(`${BASE_URL}/payroll/sheet/user/${userId}`, { headers });
  if (!payrollRes.ok) throw new Error("Payroll not found");

  const payroll = await payrollRes.json();
  return payroll.id;  // Final dynamic payroll_id used in submission
}

// === Add Appraisal using Username ===
async function addAppraisal() {
  const username = document.getElementById("appraisal-username").value.trim();
  const amountRaw = document.getElementById("appraisal-amount").value.trim();
  const amount = parseFloat(amountRaw);

  if (!username || isNaN(amount)) {
    Swal.fire("Error", "Please enter a valid username and amount", "error");
    return;
  }

  try {
    const payrollId = await getPayrollIdByUsername(username);

    console.log("POST /appraisals/add payload:", {
      payroll_id: payrollId,
      amount: amount
    });

    const res = await fetch(`${BASE_URL}/appraisals/add`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        payroll_id: payrollId,
        amount: amount
      })
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Failed to add appraisal");
    }

    const data = await res.json();
    Swal.fire("Success", `Appraisal added for ${username}`, "success");
  } catch (err) {
    Swal.fire("Error", err.message, "error");
  }
}


// === Add Penalty using Username ===
async function addPenalty() {
  const username = document.getElementById("penalty-username").value.trim();
  const amount = document.getElementById("penalty-amount").value;
  const reason = document.getElementById("penalty-reason").value;

  try {
    const payrollId = await getPayrollIdByUsername(username);

    fetch(`${BASE_URL}/penalties/add`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        payroll_id: Number(payrollId),
        amount: Number(amount),
        reason
      })
    })
    .then(res => res.json())
    .then(data => {
      Swal.fire("Success", `Penalty added for ${username}`, "success");
    });
  } catch (err) {
    Swal.fire("Error", err.message, "error");
  }
}

// === Fetch Appraisals by Username ===
async function fetchUserAppraisals() {
  const username = document.getElementById("username-input").value.trim();

  try {
    const userId = await getUserIdByUsername(username);

    fetch(`${BASE_URL}/appraisals/user/${userId}`, { headers })
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("appraisal-results");

        if (Array.isArray(data)) {
          container.innerHTML = `
            <p><strong>Username:</strong> ${username}</p>
            ${createAppraisalTable(data)}
          `;
        } else {
          container.innerHTML = `
            <p><strong>Username:</strong> ${username}</p>
            <p>No appraisals found.</p>
          `;
        }
      });
  } catch (err) {
    Swal.fire("Error", "User not found", "error");
  }
}

// === Fetch Penalties by Username ===
async function fetchUserPenalties() {
  const username = document.getElementById("username-input").value.trim();

  try {
    const userId = await getUserIdByUsername(username);

    fetch(`${BASE_URL}/penalties/user/${userId}`, { headers })
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("penalty-results");
        const formatted = Array.isArray(data) ? data : [data];

        if (formatted.length && formatted[0].id) {
          container.innerHTML = `
            <p><strong>Username:</strong> ${username}</p>
            ${createPenaltyTable(formatted)}
          `;
        } else {
          container.innerHTML = `
            <p><strong>Username:</strong> ${username}</p>
            <p>No penalties found.</p>
          `;
        }
      });
  } catch (err) {
    Swal.fire("Error", "User not found", "error");
  }
}

// === Render Appraisal Table ===
function createAppraisalTable(appraisals) {
  const rows = appraisals.map(app => `
    <tr>
      <td>${app.id}</td>
      <td>${app.payroll_id}</td>
      <td>${app.amount}</td>
      <td>${new Date(app.appraisal_date).toLocaleString()}</td>
    </tr>
  `).join("");

  return `
    <h4>Appraisals</h4>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Payroll ID</th>
          <th>Amount</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

// === Render Penalty Table ===
function createPenaltyTable(penalties) {
  const rows = penalties.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${p.payroll_id}</td>
      <td>${p.amount}</td>
      <td>${p.reason}</td>
    </tr>
  `).join("");

  return `
    <h4>Penalties</h4>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Payroll ID</th>
          <th>Amount</th>
          <th>Reason</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}
