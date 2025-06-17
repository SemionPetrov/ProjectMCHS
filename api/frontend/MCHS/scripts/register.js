const API_BASE = "http://localhost:8000/api";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const login = form.login.value.trim();
        const password = form.password.value;
        const confirmPassword = form.confirmPassword.value;

        // Валидация пароля
        if (password !== confirmPassword) {
            alert("Пароли не совпадают");
            return;
        }

        const username = `${login}`; // или любая логика

        try {
            const response = await fetch(`${API_BASE}/auth/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body: JSON.stringify({
                    username,
                    password
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail?.[0]?.msg || "Ошибка при регистрации");
            }

            const result = await response.json();
            alert(`Пользователь ${result.user_login} успешно создан!`);

            window.location.href = "/MCHS/index/user-dashboard.html"; // переход к логину
        } catch (error) {
            alert("Ошибка: " + error.message);
            console.error("Ошибка регистрации:", error);
        }
    });
});
