const API_BASE = "http://localhost:8000/api";
const token = localStorage.getItem("token");

document.addEventListener('DOMContentLoaded', () => {
    if (!token) {
        alert("Вы не авторизованы");
        window.location.href = "/MCHS/index/login.html";
        return;
    }

    const logoutBtn = document.getElementById('logoutButton');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem("token");
            window.location.href = "/MCHS/index/login.html";
        });
    }

    fetch(`${API_BASE}/user/me`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) throw new Error("Ошибка авторизации");
            return response.json();
        })
        .then(data => {
            console.log("Данные пользователя:", data);
            showUserInfo(data);
        })
        .catch(error => {
            console.error("Ошибка при получении информации о пользователе:", error);
            alert("Ошибка авторизации. Пожалуйста, войдите заново.");
            localStorage.removeItem("token");
            window.location.href = "/MCHS/index/login.html";
        });

    document.querySelectorAll('.panel-header').forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            if (content) {
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});

function showUserInfo(data) {
    if (!data || !data.employee) return;

    // Найдем или создадим элемент h1 с id userTitle
    let h1 = document.querySelector("h1#userTitle");
    if (!h1) {
        h1 = document.createElement("h1");
        h1.id = "userTitle";
        document.body.prepend(h1);
    }

    h1.textContent = `Личный кабинет: ${data.employee.last_name} ${data.employee.first_name}`;
}
