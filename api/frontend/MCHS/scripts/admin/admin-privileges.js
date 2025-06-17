const API_BASE = 'http://localhost:8000';

async function fetchWithAuth(url, method = 'GET', body = null) {
    const token = localStorage.getItem('token');
    const headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    };
    if (method === 'POST') headers['Content-Type'] = 'application/json';

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`Ошибка ${response.status}`);
    return response.json();
}

async function loadPrivilegesTable() {
    try {
        const privileges = await fetchWithAuth(`${API_BASE}/api/admin/privileges/all`);

        const usersMap = new Map();
        for (const item of privileges) {
            if (!usersMap.has(item.user_id)) {
                usersMap.set(item.user_id, {
                    login: item.login,
                    user_id: item.user_id,
                    privileges: [],
                });
            }
            if (item.privilege_id && item.privilege_name) {
                usersMap.get(item.user_id).privileges.push({
                    id: item.privilege_id,
                    name: item.privilege_name,
                });
            }
        }

        const allPrivileges = Array.from(new Map(
            privileges
                .filter(p => p.privilege_id && p.privilege_name)
                .map(p => [p.privilege_id, { id: p.privilege_id, name: p.privilege_name }])
        ).values());

        const tableBody = document.querySelector('#privilegesTable tbody');
        tableBody.innerHTML = '';

        for (const [userId, user] of usersMap.entries()) {
            const row = document.createElement('tr');

            const tdName = document.createElement('td');
            tdName.textContent = `${user.login} (ID: ${userId})`;

            const tdPrivileges = document.createElement('td');
            user.privileges.forEach(p => {
                const span = document.createElement('span');
                span.textContent = p.name;
                span.classList.add('privilege-item');

                const delBtn = document.createElement('button');
                delBtn.textContent = '❌';
                delBtn.onclick = () => deletePrivilege(userId, p.id);

                span.appendChild(delBtn);
                tdPrivileges.appendChild(span);
            });

            const tdAssign = document.createElement('td');
            const select = document.createElement('select');
            const optionEmpty = document.createElement('option');
            optionEmpty.textContent = 'Выберите привилегию';
            optionEmpty.disabled = true;
            optionEmpty.selected = true;
            select.appendChild(optionEmpty);

            allPrivileges.forEach(p => {
                const option = document.createElement('option');
                option.value = p.id;
                option.textContent = p.name;
                select.appendChild(option);
            });

            const assignBtn = document.createElement('button');
            assignBtn.textContent = 'Назначить';
            assignBtn.onclick = () => {
                if (select.value) assignPrivilege(userId, select.value);
            };

            tdAssign.appendChild(select);
            tdAssign.appendChild(assignBtn);

            row.appendChild(tdName);
            row.appendChild(tdPrivileges);
            row.appendChild(tdAssign);
            tableBody.appendChild(row);
        }

    } catch (err) {
        console.error(err);
        alert('Ошибка загрузки данных: ' + err.message);
    }
}

async function assignPrivilege(userId, privilegeId) {
    try {
        await fetchWithAuth(`${API_BASE}/api/admin/privileges/${userId}/${privilegeId}`, 'POST');
        await loadPrivilegesTable();
    } catch (err) {
        alert('Ошибка назначения привилегии: ' + err.message);
    }
}

async function deletePrivilege(userId, privilegeId) {
    try {
        await fetchWithAuth(`${API_BASE}/api/admin/privileges/${userId}/${privilegeId}`, 'DELETE');
        await loadPrivilegesTable();
    } catch (err) {
        alert('Ошибка удаления привилегии: ' + err.message);
    }
}

async function createPrivilege() {
    const name = document.getElementById('newPrivilegeName').value.trim();
    if (!name) return alert('Введите название привилегии');

    try {
        await fetchWithAuth(`${API_BASE}/api/admin/privileges/create/${encodeURIComponent(name)}`, 'POST');
        document.getElementById('newPrivilegeName').value = '';
        await loadPrivilegesTable();
    } catch (err) {
        alert('Ошибка создания привилегии: ' + err.message);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Вы не авторизованы');
        window.location.href = '/MCHS/index/login.html';
        return;
    }

    document.getElementById('logoutButton').addEventListener('click', () => {
        //localStorage.removeItem('token');
        window.location.href = '/MCHS/index/admin-dashboard.html';
    });

    document.getElementById('createPrivilegeBtn').addEventListener('click', createPrivilege);

    loadPrivilegesTable();
});
