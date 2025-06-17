const API_BASE = 'http://localhost:8000'; // Укажи актуальный адрес, если отличается

// Создание вложенной таблицы из объекта
function createTableFromObject(obj) {
    const table = document.createElement('table');
    table.classList.add('nested-table');

    for (const [key, value] of Object.entries(obj)) {
        const row = document.createElement('tr');

        const tdKey = document.createElement('td');
        tdKey.textContent = key;

        const tdValue = document.createElement('td');

        if (typeof value === 'object' && value !== null) {
            tdValue.textContent = 'Нажмите для просмотра';
            tdValue.classList.add('object-toggle');

            tdValue.addEventListener('click', function () {
                if (tdValue.dataset.expanded === 'true') {
                    tdValue.innerHTML = 'Нажмите для просмотра';
                    tdValue.dataset.expanded = 'false';
                } else {
                    const nested = createTableFromObject(value);
                    tdValue.innerHTML = '';
                    tdValue.appendChild(nested);
                    tdValue.dataset.expanded = 'true';
                }
            });
        } else {
            tdValue.textContent = value;
        }

        row.appendChild(tdKey);
        row.appendChild(tdValue);
        table.appendChild(row);
    }

    return table;
}

// Загрузка технической информации
async function loadTechInfo() {
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Вы не авторизованы!');
        window.location.href = '/MCHS/index/login.html';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/admin/dashboard`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        });

        if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);

        const data = await response.json();

        const tbody = document.querySelector('#techInfoTable tbody');
        tbody.innerHTML = '';

        for (const [key, value] of Object.entries(data)) {
            const row = document.createElement('tr');

            const tdKey = document.createElement('td');
            tdKey.textContent = key;

            const tdValue = document.createElement('td');

            if (typeof value === 'object' && value !== null) {
                tdValue.textContent = 'Нажмите для просмотра';
                tdValue.classList.add('object-toggle');

                tdValue.addEventListener('click', function () {
                    if (tdValue.dataset.expanded === 'true') {
                        tdValue.innerHTML = 'Нажмите для просмотра';
                        tdValue.dataset.expanded = 'false';
                    } else {
                        const nested = createTableFromObject(value);
                        tdValue.innerHTML = '';
                        tdValue.appendChild(nested);
                        tdValue.dataset.expanded = 'true';
                    }
                });
            } else {
                tdValue.textContent = value;
            }

            row.appendChild(tdKey);
            row.appendChild(tdValue);
            tbody.appendChild(row);
        }

    } catch (err) {
        alert('Ошибка загрузки информации: ' + err.message);
    }
}

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    loadTechInfo();

    document.getElementById('logoutButton')?.addEventListener('click', () => {
        //localStorage.removeItem('token');
        window.location.href = '/MCHS/index/admin-dashboard.html';
    });
});
