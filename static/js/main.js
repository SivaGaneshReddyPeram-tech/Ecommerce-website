document.querySelectorAll('.messages').forEach((container) => {
  setTimeout(() => container.classList.add('is-hidden'), 4000);
});
