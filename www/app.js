$(document).on("keypress", function(event) {
    Shiny.setInputValue("keyid", event.keyCode);
});

window.addEventListener('message', function(e) {
    // Check the origin of the sender
    if (e.data === 'light-mode') {
        document.documentElement.dataset.bsTheme = "light";
        document.documentElement.style.setProperty('--bs-body-bg', "#f9fffe");
    } else if (e.data === 'dark-mode') {
        document.documentElement.dataset.bsTheme = "dark";
        document.documentElement.style.setProperty('--bs-body-bg', "#16242f");
    }
  }, false);


window.parent.postMessage('ShinyColorQuery', '*');