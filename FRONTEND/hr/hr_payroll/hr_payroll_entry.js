document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  if (!token) {
    Swal.fire({
      icon: "warning",
      title: "Unauthorized",
      text: "Please log in first.",
    }).then(() => {
      window.location.href = "/../frontend/login/login.html";
    });
  }
  
});
