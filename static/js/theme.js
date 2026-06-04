const themeToggle = document.getElementById('themeToggle');
const savedTheme = localStorage.getItem('theme');

if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
} else if (savedTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}