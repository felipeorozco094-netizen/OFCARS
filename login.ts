document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector<HTMLFormElement>("#admin-login-form");
    const message = document.querySelector<HTMLElement>("#login-demo-message");
    if (!form || !message) return;

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;
        message.textContent = "Acceso de demostración. La autenticación se conectará con Python.";
        message.hidden = false;
        window.setTimeout(() => { window.location.href = "admin.html"; }, 600);
    });
});
