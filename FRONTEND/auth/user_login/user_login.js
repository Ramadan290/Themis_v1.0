document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();

        // ✅ Save token with correct Bearer prefix
        localStorage.setItem('token', `Bearer ${data.access_token}`);

        // ✅ Decode JWT and extract role
        const payload = JSON.parse(atob(data.access_token.split('.')[1]));
        const role = payload.role;
        localStorage.setItem('role', role);

        // ✅ Redirect by role
        if (role === 'employee') {
          window.location.href = '../../employee/employee_portal/employee_portal.html';
        } else if (role === 'hr') {
          window.location.href = '../../hr/hr_portal/hr_portal.html';
        } else if (role === 'admin') {
          window.location.href = '/../frontend/admin/portal/portal.html';
        } else {
          errorMessage.textContent = 'Unknown role. Access denied.';
        }
      } else {
        const errorData = await response.json();
        errorMessage.textContent = errorData.detail || 'Login failed.';
      }
    } catch (error) {
      console.error('Error during login:', error);
      errorMessage.textContent = 'An error occurred. Please try again.';
    }
  });
});
