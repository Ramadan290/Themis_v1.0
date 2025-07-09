
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
        usernameElement.textContent = 'HR';
      }
    }
  
    // Add click events to boxes for navigation
    document.getElementById('payroll-box').addEventListener('click', () => {
      window.location.href = '/hr/payroll/payroll.html';
    });
  
    document.getElementById('attendance-box').addEventListener('click', () => {
      window.location.href = '/hr/attendance/attendance.html';
    });
  
    document.getElementById('news-box').addEventListener('click', () => {
      window.location.href = '/hr/news/news.html';
    });
  
    document.getElementById('status-box').addEventListener('click', () => {
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


      const dateElement = document.getElementById("today-date");
    const timeElement = document.getElementById("local-time");
    const weatherElement = document.getElementById("weather");

    // Set date
    const today = new Date();
    dateElement.textContent = today.toDateString();

    // Set time and keep updating it
    setInterval(() => {
      const now = new Date();
      timeElement.textContent = now.toLocaleTimeString();
    }, 1000);

    // Simulated weather (rotates daily)
    const simulatedWeather = [
      "Sunny, 33°C ☀️",
      "Cloudy, 28°C ☁️",
      "Rainy, 24°C 🌧️",
      "Windy, 26°C 🌬️",
      "Foggy, 22°C 🌫️"
    ];
    const day = new Date().getDay(); // 0 - Sunday, 6 - Saturday
    weatherElement.textContent = simulatedWeather[day % simulatedWeather.length];