
document.addEventListener('DOMContentLoaded', () => {
    // Decode the access token to get the username
    const token = localStorage.getItem('token');
    const usernameElement = document.getElementById('username');
  
    if (token) {
      try {
        // Decode the JWT token
        const payload = JSON.parse(atob(token.split('.')[1])); // Decode the payload
        const username = payload.sub; // 'sub' contains the username
        usernameElement.textContent = username;
      } catch (error) {
        console.error('Invalid token:', error);
        usernameElement.textContent = 'Employee';
      }
    }
  
    // Add click events to boxes for navigation
    document.getElementById('payroll-box').addEventListener('click', () => {
      window.location.href = '/Frontend/employee/employee_payroll/payroll.html';
    });
  
    document.getElementById('attendance-box').addEventListener('click', () => {
      window.location.href = '/Frontend/employee/employee_attendance/attendance.html';
    });
  
    document.getElementById('news-box').addEventListener('click', () => {
      window.location.href = '/Frontend/employee/employee_news/news.html';
    });
  
    document.getElementById('status-box').addEventListener('click', () => {
      // Show a SweetAlert with a custom message
      Swal.fire({
        background: "linear-gradient(to bottom, #41295a, #2f0743) ",
        icon: "error",
        title: "Oops...",
        color: "white",
        text: "'Status page is under construction!'",
        confirmButtonText: "OK",
      });
    });
  
    // Logout button functionality
    document.getElementById('logout-button').addEventListener('click', () => {
      localStorage.removeItem('token'); // Clear the access token
      window.location.href = '../../auth/user_login/user_login.html'; // Redirect to login page
    });
  });