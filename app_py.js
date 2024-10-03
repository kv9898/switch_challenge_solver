// shiny keypress
$(document).on("keypress", function(event) {
    Shiny.setInputValue("keyid", event.keyCode);
});
// colour mode
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

// own sortableJS script
document.addEventListener("DOMContentLoaded", function() {
    var el_ini = document.getElementById('initial');
    if (el_ini) {  // Check if element exists
        var sortable_ini = new Sortable(el_ini, {
            animation: 150,  // Optional animation speed
            ghostClass: 'sortable-ghost',  // Class name for the placeholder element during drag
            chosenClass: 'sortable-chosen', // Class name for the chosen item
            onSort: function (evt) {
                var order = sortable_ini.toArray();
                Shiny.setInputValue("initial", order);
            }
        });
    } else {
        console.error("Element with id 'initial' not found");
    }
    var el_fin = document.getElementById('final');
    if (el_fin) {  // Check if element exists
        var sortable_fin = new Sortable(el_fin, {
            animation: 150,  // Optional animation speed
            ghostClass: 'sortable-ghost',  // Class name for the placeholder element during drag
            chosenClass: 'sortable-chosen', // Class name for the chosen item
            onSort: function (evt) {
                var order = sortable_fin.toArray();
                Shiny.setInputValue("final", order);
            }
        });
    } else {
        console.error("Element with id 'initial' not found");
    }
});