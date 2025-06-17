const API_BASE = "http://localhost:8000/api";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", () => {
    if (!token) {
        alert("Вы не авторизованы");
        window.location.href = "/MCHS/index/login.html";
        return;
    }

    document.getElementById("logoutButton").addEventListener("click", () => {
        window.location.href = "/MCHS/index/user-dashboard.html";
    });

    fetch(`${API_BASE}/user/attestations`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) throw new Error("Ошибка загрузки аттестаций");
            return response.json();
        })
        .then(data => renderAttestations(data))
        .catch(err => {
            console.error(err);
            document.getElementById("attestationsList").textContent = "Не удалось загрузить данные.";
        });
});

function renderAttestations(response) {
    const container = document.getElementById("attestationsList");
    container.innerHTML = "";

    const attestations = response.data;

    if (!attestations || attestations.length === 0) {
        container.textContent = "Аттестации не найдены.";
        return;
    }

    attestations.forEach(item => {
        const div = document.createElement("div");
        div.className = "attestation-item";
        div.innerHTML = `
      <strong>Название:</strong> ${item.title || '—'}<br>
      <strong>Дата:</strong> ${item.date || '—'}<br>
      <strong>Статус:</strong> ${item.status || '—'}<br>
      <hr />
    `;
        container.appendChild(div);
    });
}

