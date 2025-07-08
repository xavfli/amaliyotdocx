// Tungi rejimni yoqish/o‘chirish
function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle("dark-mode");

    // Saqlash uchun localStorage
    if (body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

// Sahifa yuklanganda foydalanuvchi tanlovini tiklash
window.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});
