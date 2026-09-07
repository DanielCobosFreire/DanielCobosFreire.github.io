document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      const mensaje = form.dataset.confirm || '¿Desea continuar?';
      if (!window.confirm(mensaje)) event.preventDefault();
    });
  });
});
