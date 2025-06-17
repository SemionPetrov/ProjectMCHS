// Переключение между вкладками "Вход" и "Регистрация"
function switchTab(tabName) {
  document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
  document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add('active');
  document.getElementById(`${tabName}-section`).classList.add('active');
}

document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('loginForm');

  loginForm?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(loginForm);
    const data = Object.fromEntries(formData.entries());

    // Подготовка данных в формате application/x-www-form-urlencoded
    const encodedData = new URLSearchParams();
    encodedData.append('grant_type', 'password');
    encodedData.append('username', data.username);
    encodedData.append('password', data.password);
    encodedData.append('scope', '');
    encodedData.append('client_id', '');
    encodedData.append('client_secret', '');

    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        },
        body: encodedData.toString()
      });

      const result = await response.json();
      console.log("Ответ от сервера:", result);

      if (!response.ok) {
        const detail = Array.isArray(result.detail)
            ? result.detail.map(err => err.msg).join(", ")
            : result.detail || "Неизвестная ошибка";
        alert("Ошибка входа: " + detail);
        return;
      }

      // ✅ Сохраняем токен
      localStorage.setItem('token', result.access_token);

      alert("Успешный вход!");

      // Переход в зависимости от роли
      if (result.role === 'admin') {
        window.location.href = '/index/admin-dashboard.html';
      } else {
        window.location.href = '/index/user-dashboard.html';
      }

    } catch (err) {
      console.error("Ошибка:", err);
      alert("Ошибка подключения к серверу.");
    }
  });
});
