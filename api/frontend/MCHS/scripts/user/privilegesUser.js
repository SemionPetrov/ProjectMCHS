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

    fetch(`${API_BASE}/user/privileges`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) throw new Error("Ошибка при загрузке привилегий");
            return response.json();
        })
        .then(data => {
            console.log("Привилегии:", data);
            renderPrivileges(data);
        })
        .catch(error => {
            console.error(error);
            document.getElementById("privilegesContainer").textContent = "Не удалось загрузить привилегии.";
        });
});

function renderPrivileges(response) {
    const privileges = response.privileges;
    const container = document.getElementById("privilegesContainer");
    container.innerHTML = "";

    if (!privileges || privileges.length === 0) {
        container.innerHTML = "<p>Нет привилегий</p>";
        return;
    }

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    thead.innerHTML = `
    <tr>
      <th>№</th>
      <th>Привилегия</th>
    </tr>
  `;
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    privileges.forEach((priv, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${index + 1}</td>
      <td>${priv}</td>
    `;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}
