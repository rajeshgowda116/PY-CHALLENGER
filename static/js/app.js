document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        document.querySelectorAll(".toast-stack .alert").forEach((alert) => {
            alert.classList.add("fade");
            setTimeout(() => alert.remove(), 400);
        });
    }, 3500);
});
