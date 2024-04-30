function toggleDropdown() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.classList.toggle('hidden'); 
}

document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('user-dropdown');
    const userIcon = document.getElementById('user-icon');

    if (!userIcon.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add('hidden'); 
    }
});
