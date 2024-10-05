$(document).on("keypress", function(event) {
    Shiny.setInputValue("keyid", event.keyCode);
});

//window.parent.addEventListener("quarto-color-mode", function(event) {
  // Shiny.setInputValue('quarto_mode', event.detail.mode);
//  document.documentElement.dataset.bsTheme = event.detail.mode;
//  if (event.detail.mode === "dark") {
//      document.documentElement.style.setProperty('--bs-body-bg', "#16242f");
//  }  else if (event.detail.mode === "light") {
//      document.documentElement.style.setProperty('--bs-body-bg', "#f9fffe");
//  }
//})

window.addEventListener('message', function(e) {
    // Check the origin of the sender
    alert(e.data);
    if (e.data === 'light-mode') {
        document.documentElement.style.setProperty('--bs-body-bg', "#f9fffe");
    } else if (e.data === 'dark-mode') {
        document.documentElement.style.setProperty('--bs-body-bg', "#16242f");
    }
  }, false);


window.parent.postMessage('ShinyColorQuery', '*');