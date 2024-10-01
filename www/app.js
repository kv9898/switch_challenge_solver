$(document).on("keypress", function(event) {
    Shiny.setInputValue("keyid", event.keyCode);
});

window.parent.addEventListener("quarto-color-mode", function(event) {
  // Shiny.setInputValue('quarto_mode', event.detail.mode);
  document.documentElement.dataset.bsTheme = event.detail.mode;
  if (event.detail.mode === "dark") {
      document.documentElement.style.setProperty('--bs-body-bg', "#16242f");
  }  else if (event.detail.mode === "light") {
      document.documentElement.style.setProperty('--bs-body-bg', "#f9fffe");
  }
})
window.parent.postMessage('ShinyColorQuery', '*');