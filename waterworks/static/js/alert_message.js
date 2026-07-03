setTimeout(() => {
    const toasts = document.querySelectorAll('.toast-item');
    toasts.forEach(t => t.remove());
}, 5000);
