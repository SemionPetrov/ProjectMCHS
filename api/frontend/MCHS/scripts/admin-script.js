document.addEventListener('DOMContentLoaded', () => {
    // Обработчик кнопки выхода
    document.getElementById('logoutButton').addEventListener('click', () => {
        window.location.href = '/MCHS/index/login.html';
    });

    // Обработчики переходов по кнопкам
    document.getElementById('techInfoButton').addEventListener('click', () => {
        window.location.href = '/MCHS/index/administration/tech-info.html';
    });

    document.getElementById('databaseButton').addEventListener('click', () => {
        window.location.href = '/MCHS/index/administration/admin-database.html';
    });

    document.getElementById('privilegesButton').addEventListener('click', () => {
        window.location.href = '/MCHS/index/administration/privileges.html';
    });
});
