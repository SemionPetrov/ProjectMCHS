const BASE_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logoutButton');
    logoutButton.addEventListener('click', () => {
        //localStorage.removeItem('token');
        window.location.href = '/MCHS/index/user-dashboard.html';
    });

    loadPendingExercises();
});

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Токен не найден. Пожалуйста, авторизуйтесь.');
        window.location.href = '/MCHS/index/login.html';
        return;
    }

    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
    };

    const response = await fetch(BASE_URL + url, {
        ...options,
        headers
    });

    const text = await response.text();

    try {
        return JSON.parse(text);
    } catch (e) {
        console.error('Ошибка парсинга JSON:', e);
        return null;
    }
}

async function loadPendingExercises() {
    const container = document.getElementById('pending-exercises-container');
    const message = document.getElementById('message');

    container.innerHTML = '';
    message.textContent = 'Загрузка...';

    const result = await fetchWithAuth('/api/user/exercises');

    if (!result || !result.success) {
        message.textContent = 'Ошибка загрузки данных.';
        return;
    }

    const exercises = result.data;

    if (!exercises || exercises.length === 0) {
        message.textContent = 'Нет запланированных событий.';
        return;
    }

    message.textContent = '';

    exercises.forEach(ex => {
        const div = document.createElement('div');
        div.className = 'exercise-item';

        div.innerHTML = `
            <h3>${ex.type_name}</h3>
            <p><strong>Дата:</strong> ${new Date(ex.date).toLocaleString()}</p>
            <p><strong>Адрес:</strong> ${ex.address}</p>
            <p><strong>Комментарий:</strong> ${ex.comment || '—'}</p>
        `;

        container.appendChild(div);
    });
}
