const token = localStorage.getItem("token");

// Load news on page load
document.addEventListener("DOMContentLoaded", () => {
  fetchNews();
});

// ========== Fetch All News ==========
async function fetchNews() {
  const newsList = document.getElementById("newsList");
  newsList.innerHTML = "";

  try {
    const response = await fetch("http://127.0.0.1:8000/news/all", {
      headers: { Authorization: token }
    });

    if (!response.ok) throw new Error("Failed to fetch news");

    const newsArray = await response.json();

    for (const news of newsArray) {
      const li = document.createElement("li");

      // Fetch comments for this news separately
      let commentsHtml = "<li>Loading comments...</li>";
      try {
        const commentsRes = await fetch(`http://127.0.0.1:8000/comment/news/${news.id}`, {
          headers: { Authorization: token }
        });

        if (commentsRes.ok) {
          const comments = await commentsRes.json();

          commentsHtml = comments.length
            ? comments.map(c => `
                <li>
                  ${c.content} - <i>${c.username}</i>
                  <button onclick="deleteComment(${c.id})">🗑 Delete</button>
                </li>`).join("")
            : "<li>No comments yet.</li>";
        } else {
          commentsHtml = "<li>Failed to load comments</li>";
        }
      } catch {
        commentsHtml = "<li>Error loading comments</li>";
      }

      li.innerHTML = `
        <h4>${news.title}</h4>
        <p>${news.content}</p>
        <small><b>By:</b> ${news.author} | <b>Posted:</b> ${news.posted_at}</small><br><br>
        <button onclick="deleteNews(${news.id})">🗑 Delete News</button>

        <h5>Comments:</h5>
        <ul>${commentsHtml}</ul>

        <!-- New Comment Form -->
        <input type="text" id="comment-input-${news.id}" placeholder="Write a comment..." />
        <button onclick="postComment(${news.id})">Post Comment</button>
      `;

      newsList.appendChild(li);
    }

  } catch (err) {
    console.error("Error loading news:", err);
    Swal.fire("Error", "Failed to load news", "error");
  }
}

// ========== Add News ==========
document.getElementById("newsForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const title = document.getElementById("news-title").value.trim();
  const content = document.getElementById("news-content").value.trim();

  if (!title || !content) {
    Swal.fire("Error", "Please fill in both title and content.", "error");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/news/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": token
      },
      body: JSON.stringify({ title, content })
    });

    if (!res.ok) throw new Error("Failed to add news");

    Swal.fire("Success", "News added successfully!", "success");
    document.getElementById("newsForm").reset();
    fetchNews();

  } catch (err) {
    console.error("Error adding news:", err);
    Swal.fire("Error", "Could not add news", "error");
  }
});

// ========== Delete News ==========
async function deleteNews(id) {
  const confirm = await Swal.fire({
    title: "Are you sure?",
    text: "This will permanently delete the news post.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, delete it",
    cancelButtonText: "Cancel"
  });

  if (!confirm.isConfirmed) return;

  try {
    const res = await fetch(`http://127.0.0.1:8000/news/delete/${id}`, {
      method: "DELETE",
      headers: { Authorization: token }
    });

    const result = await res.json();

    if (res.ok) {
      Swal.fire("Deleted", result.detail, "success");
      fetchNews();
    } else {
      Swal.fire("Error", result.detail || "Failed to delete news", "error");
    }

  } catch (err) {
    console.error("Delete news error:", err);
    Swal.fire("Error", "Failed to delete news", "error");
  }
}

// ========== Post Comment ==========
async function postComment(newsId) {
  const input = document.getElementById(`comment-input-${newsId}`);
  const content = input.value.trim();
  if (!content) {
    Swal.fire("Error", "Comment cannot be empty", "error");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/comment/post", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": token
      },
      body: JSON.stringify({
        news_id: newsId,
        content: content
      })
    });

    if (!res.ok) throw new Error("Failed to post comment");

    Swal.fire("Success", "Comment posted!", "success");
    input.value = "";
    fetchNews();

  } catch (err) {
    console.error("Error posting comment:", err);
    Swal.fire("Error", "Could not post comment", "error");
  }
}

// ========== Delete Comment ==========
async function deleteComment(commentId) {
  const confirm = await Swal.fire({
    title: "Are you sure?",
    text: "This will permanently delete the comment.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, delete it",
    cancelButtonText: "Cancel"
  });

  if (!confirm.isConfirmed) return;

  try {
    const res = await fetch(`http://127.0.0.1:8000/comment/delete/${commentId}`, {
      method: "DELETE",
      headers: { Authorization: token }
    });

    const result = await res.json();

    if (res.ok) {
      Swal.fire("Deleted", result.detail, "success");
      fetchNews();
    } else {
      Swal.fire("Error", result.detail || "Permission denied", "error");
    }

  } catch (err) {
    console.error("Delete comment error:", err);
    Swal.fire("Error", "Failed to delete comment", "error");
  }
}
