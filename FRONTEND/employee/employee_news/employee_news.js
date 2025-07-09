document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("user_id");
  const newsContainer = document.getElementById("news-container");
  const newsDetails = document.getElementById("news-details");
  const commentsList = document.getElementById("comments-list");
  const commentForm = document.getElementById("comment-form");

  let selectedNewsId = null;

  // Load all news
  async function loadNews() {
    try {
      const response = await fetch("http://127.0.0.1:8000/news/all", {
        headers: { Authorization: token },
      });

      const newsList = await response.json();
      newsContainer.innerHTML = "";

      newsList.forEach((news) => {
        const div = document.createElement("div");
        div.className = "news-item";
        div.innerHTML = `
          <h3>${news.title}</h3>
          <p>${news.content}</p>
          <small>By ${news.author} | ${news.posted_at}</small><br>
          <button onclick="viewDetails(${news.id}, \`${news.title}\`, \`${news.content}\`, \`${news.author}\`, \`${news.posted_at}\`)">View</button>
        `;
        newsContainer.appendChild(div);
      });
    } catch (err) {
      console.error("Failed to load news:", err);
    }
  }

  window.viewDetails = async (id, title, content, author, postedAt) => {
    selectedNewsId = id;
    document.getElementById("news-title").innerText = title;
    document.getElementById("news-content").innerText = content;
    document.getElementById("news-author").innerText = author;
    document.getElementById("news-date").innerText = postedAt;
    newsDetails.style.display = "block";
    await loadComments(id);
  };

  async function loadComments(newsId) {
    commentsList.innerHTML = "";
    try {
      const response = await fetch("http://127.0.0.1:8000/comment/news/" + newsId, {
        headers: { Authorization: token },
      });
      const comments = await response.json();

      comments.forEach((c) => {
        const li = document.createElement("li");
li.innerHTML = `
  <strong>${c.username}:</strong> ${c.content}
  <br><small>(${c.commented_at})</small>
  ${c.user_id == userId ? `<button onclick="deleteComment(${c.id})">🗑️</button>` : ""}
`;
        commentsList.appendChild(li);
      });
    } catch (error) {
      console.error("Error loading comments:", error);
    }
  }

  commentForm.onsubmit = async (e) => {
    e.preventDefault();
    const content = document.getElementById("comment-content").value;

    try {
      const res = await fetch("http://127.0.0.1:8000/comment/post", {
        method: "POST",
        headers: {
          Authorization: token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          news_id: selectedNewsId,
          content: content,
        }),
      });

      if (res.ok) {
        commentForm.reset();
        await loadComments(selectedNewsId);
      } else {
        Swal.fire("Error", "Failed to post comment", "error");
      }
    } catch (err) {
      console.error("Comment failed:", err);
    }
  };

  window.deleteComment = async (commentId) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/comment/delete/${commentId}`, {
        method: "DELETE",
        headers: {
          Authorization: token,
        },
      });

      const result = await res.json();

      if (res.ok) {
        await loadComments(selectedNewsId);
        Swal.fire("Deleted!", result.detail, "success");
      } else {
        Swal.fire("Denied", result.detail || "Unauthorized", "warning");
      }
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  loadNews();
});
