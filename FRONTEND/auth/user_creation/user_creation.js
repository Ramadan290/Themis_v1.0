document.getElementById('register-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  const confirmPassword = document.getElementById('confirm-password').value.trim();
  const role = document.getElementById('role').value;
  const errorMessage = document.getElementById('error-message');

  errorMessage.textContent = "";

  if (password !== confirmPassword) {
    errorMessage.textContent = "Passwords do not match!";
    return;
  }

  if (!role) {
    errorMessage.textContent = "Please select a role.";
    return;
  }

  const token = localStorage.getItem('token');

  try {
    const response = await fetch('/auth/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ username, password, role }),
    });

    if (response.ok) {
      alert('Registration successful! Redirecting to login...');
      window.location.href = '/login.html';
    } else {
      const error = await response.json();
      errorMessage.textContent = error.detail || 'Registration failed.';
    }
  } catch (error) {
    console.error('Registration error:', error);
    errorMessage.textContent = 'An error occurred. Please try again.';
  }
});
