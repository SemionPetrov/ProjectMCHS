const API_BASE = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('queryResult');
    const button = document.getElementById('runQueryButton');
    const queryInput = document.getElementById('sqlQuery');

    button.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        output.innerHTML = 'Выполняется запрос...';

        if (!query) {
            output.textContent = 'Введите SQL-запрос.';
            return;
        }

        const token = localStorage.getItem('token');
        if (!token) {
            alert('Токен не найден. Авторизуйтесь снова.');
            window.location.href = '/MCHS/index/login.html';
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/api/admin/db_run_query?query=${encodeURIComponent(query)}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const result = await response.json();

            if (result.status === 'success') {
                // Преобразуем результат в таблицу
                const rows = result.results.split(',').map(item => item.trim());
                const columnsPerRowGuess = 7; // Настрой: сколько колонок в одной строке (по структуре таблицы)
                const table = document.createElement('table');
                table.className = 'result-table';

                for (let i = 0; i < rows.length; i += columnsPerRowGuess) {
                    const tr = document.createElement('tr');
                    for (let j = 0; j < columnsPerRowGuess; j++) {
                        const td = document.createElement('td');
                        td.textContent = rows[i + j] ?? '';
                        tr.appendChild(td);
                    }
                    table.appendChild(tr);
                }

                output.innerHTML = `<div><strong>Запрос:</strong> <code>${result.query}</code></div>`;
                output.appendChild(table);
            } else {
                output.innerHTML = `<span style="color:red;">Ошибка: ${result.status}</span>`;
            }
        } catch (err) {
            output.innerHTML = `<span style="color:red;">Ошибка при выполнении запроса:<br>${err.message}</span>`;
        }
    });

    document.getElementById('logoutButton').addEventListener('click', () => {
        window.location.href = '/MCHS/index/admin-dashboard.html';
    });
});
