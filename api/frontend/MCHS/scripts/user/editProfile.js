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

    const form = document.getElementById("profileForm");
    const message = document.getElementById("message");

    // Подгружаем текущие данные
    fetch(`${API_BASE}/user/me`, {
        headers: { Authorization: `Bearer ${token}` }
    })
        .then(res => {
            if (!res.ok) throw new Error("Ошибка при загрузке данных");
            return res.json();
        })
        .then(data => {
            const employee = data.employee;
            if (!employee) {
                message.textContent = "Данные сотрудника не найдены";
                return;
            }
            document.getElementById("last_name").value = employee.last_name || "";
            document.getElementById("first_name").value = employee.first_name || "";
            document.getElementById("surname").value = employee.surname || "";
            document.getElementById("birthday").value = employee.birthday || "";
            document.getElementById("rang_id").value = employee.rang_id || "";
            document.getElementById("position_id").value = employee.position_id || "";
            document.getElementById("comment").value = employee.comment || "";
        })
        .catch(err => {
            console.error(err);
            message.textContent = "Ошибка при получении данных.";
        });

    // Отправка формы
    form.addEventListener("submit", e => {
        e.preventDefault();

        const payload = {
            last_name: document.getElementById("last_name").value.trim(),
            first_name: document.getElementById("first_name").value.trim(),
            surname: document.getElementById("surname").value.trim(),
            birthday: document.getElementById("birthday").value.trim(),
            rang_id: parseInt(document.getElementById("rang_id").value) || null,
            position_id: parseInt(document.getElementById("position_id").value) || null,
            comment: document.getElementById("comment").value.trim()
        };

        // Преобразование даты birthday в формат DD.MM.YYYY
        let birthdayFormatted = "";
        if (payload.birthday) {
            const parts = payload.birthday.split("-");
            if (parts.length === 3) {
                birthdayFormatted = `${parts[2]}.${parts[1]}.${parts[0]}`;
            } else {
                birthdayFormatted = payload.birthday;
            }
        }

        const params = new URLSearchParams();
        if (payload.last_name) params.append("last_name", payload.last_name);
        if (payload.first_name) params.append("first_name", payload.first_name);
        if (payload.surname) params.append("surname", payload.surname);
        if (birthdayFormatted) params.append("birthday", birthdayFormatted);
        if (payload.position_id) params.append("position_id", payload.position_id);
        if (payload.rang_id) params.append("rang_id", payload.rang_id);
        if (payload.comment) params.append("comment", payload.comment);

        const url = `${API_BASE}/user/change_personal_data?${params.toString()}`;

        fetch(url, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`
            }

        })
            .then(res => {
                if (!res.ok) throw new Error("Ошибка при сохранении данных");
                return res.text();
            })
            .then(data => {
                console.log("Ответ от сервера при сохранении профиля:", data);
                message.textContent = "Изменения успешно сохранены";
                message.style.color = "green";

                setTimeout(() => {
                    window.location.href = "/MCHS/index/user-dashboard.html";
                }, 1000);
            })
            .catch(err => {
                console.error(err);
                message.textContent = "Ошибка при сохранении данных";
                message.style.color = "red";
            });
    });
});
