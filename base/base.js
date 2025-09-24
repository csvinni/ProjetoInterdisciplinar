document.getElementById('open_btn').addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('open-sidebar');
});

document.querySelectorAll(".submenu-toggle").forEach(toggle => {
    toggle.addEventListener("click", (e) => {
        e.preventDefault();
        const parent = toggle.parentElement;
        parent.classList.toggle("open");
    });
});
