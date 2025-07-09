let raiseRequests = [];
const userCache = {};

async function loadRaiseRequestsWithUsernames() {
  const token = localStorage.getItem("token");

  const res = await fetch("http://127.0.0.1:8000/raise/all", {
    headers: { Authorization: token }
  });
  const data = await res.json();

  const enriched = await Promise.all(
    data.map(async (req) => {
      if (!req.user_id) {
        req.username = "N/A";
        return req;
      }

      if (userCache[req.user_id]) {
        req.username = userCache[req.user_id];
        return req;
      }

      try {
        const res = await fetch(`http://127.0.0.1:8000/auth/users/by-id/${req.user_id}`, {
          headers: { Authorization: token }
        });

        if (res.ok) {
          const user = await res.json();
          userCache[req.user_id] = user.username;
          req.username = user.username;
        } else {
          req.username = "Unknown";
        }
      } catch {
        req.username = "Unknown";
      }

      return req;
    })
  );

  raiseRequests = enriched;
  renderRaiseRequests(raiseRequests);
}
function renderRaiseRequests(data) {
  const pendingTbody = document.getElementById("raise-requests-body");
  const reviewedTbody = document.getElementById("reviewed-requests-body");

  pendingTbody.innerHTML = "";
  reviewedTbody.innerHTML = "";

  data.forEach(req => {
    const row = document.createElement("tr");

    if (req.status === "pending") {
      row.innerHTML = `
        <td>${req.request_uid}</td>
        <td>${req.username}</td>
        <td>${req.requested_amount}</td>
        <td>${req.reason}</td>
        <td>${req.status}</td>
        <td>${req.requested_at || "N/A"}</td>
        <td>${req.review_comment || "-"}</td>
        <td>
          <select onchange="handleDecision(this, ${req.id})">
            <option value="">Choose</option>
            <option value="approved">Approve</option>
            <option value="rejected">Reject</option>
          </select>
        </td>
      `;
      pendingTbody.appendChild(row);
    } else {
      row.innerHTML = `
        <td>${req.request_uid}</td>
        <td>${req.username}</td>
        <td>${req.requested_amount}</td>
        <td>${req.reason}</td>
        <td>${req.status}</td>
        <td>${req.requested_at || "N/A"}</td>
        <td>${req.review_comment || "-"}</td>
      `;
      reviewedTbody.appendChild(row);
    }
  });
}


function handleDecision(select, id) {
  const value = select.value;
  if (!value) return;

  Swal.fire({
    title: `Confirm ${value}?`,
    input: 'text',
    inputLabel: 'Comment (optional)',
    showCancelButton: true,
    confirmButtonText: `Yes, ${value}`,
    preConfirm: async (comment) => {
      const token = localStorage.getItem("token");
      const res = await fetch("http://127.0.0.1:8000/raise/review", {
        method: "POST",
        headers: {
          Authorization: token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          request_id: id,
          status: value,
          review_comment: comment || ""
        })
      });

      if (res.ok) {
        Swal.fire("Success", "Request updated", "success");
        loadRaiseRequestsWithUsernames();
      } else {
        Swal.fire("Error", "Failed to update", "error");
      }
    }
  });
}

function applyUsernameFilter() {
  const query = document.getElementById("usernameFilter").value.toLowerCase().trim();
  if (query === "") {
    renderRaiseRequests(raiseRequests);
    return;
  }

  const filtered = raiseRequests.filter(req =>
    req.username && req.username.toLowerCase().includes(query)
  );
  renderRaiseRequests(filtered);
}

document.addEventListener("DOMContentLoaded", () => {
  loadRaiseRequestsWithUsernames();
});
