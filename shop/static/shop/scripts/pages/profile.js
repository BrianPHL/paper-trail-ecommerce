const initializeProfilePage = () => {
    // Dark mode logic: apply theme based on localStorage or default
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);

    // Edit form toggle logic
    const editBtn = document.getElementById('edit-profile-btn');
    const editForm = document.getElementById('edit-profile-form');
    if (editBtn && editForm) {
        editBtn.addEventListener('click', () => {
            editForm.style.display = editForm.style.display === 'none' ? 'flex' : 'none';
        });
    }
};

export default initializeProfilePage;
