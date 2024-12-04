// finction to set the user mode
function setMode(mode) {
    // remove existing mode
    document.body.classList.remove('light-mode', 'dark-mode', 'topher-mode');
    const navbar = document.querySelector('.navbar');
    const footer = document.querySelector('.footer');
    navbar.classList.remove('light-mode', 'dark-mode', 'topher-mode');
    footer.classList.remove('light-mode', 'dark-mode', 'topher-mode');

    // add selected mode
    document.body.classList.add(`${mode}-mode`);
    navbar.classList.add(`${mode}-mode`);
    footer.classList.add(`${mode}-mode`);

    // save
    localStorage.setItem('mode', mode);

    // highlight the current mode in the dropdown menu
     const modeLinks = document.querySelectorAll('#modeSwitcherMenu a');
     modeLinks.forEach(link => link.classList.remove('bg-blue-500', 'text-white')); // temove highlight
     const currentModeLink = document.querySelector(`#modeSwitcherMenu a[onclick="setMode('${mode}')"]`);
     if (currentModeLink) {
         currentModeLink.classList.add('bg-blue-500', 'text-white'); // add highlight
     }

}

// function to save mode on page
function loadMode() {
    const savedMode = localStorage.getItem('mode') || 'topher'; // topher is default mode man
    setMode(savedMode);
}

// event listener to make sure objects are loaded
document.addEventListener('DOMContentLoaded', function() {
    loadMode();

    //toggle dropdown menu 
    const modeSwitcherBtn = document.getElementById('modeSwitcherBtn');
    const modeSwitcherMenu = document.getElementById('modeSwitcherMenu');

    modeSwitcherBtn.addEventListener('click', function(event) {
        event.stopPropagation();
        modeSwitcherMenu.classList.toggle('hidden');
    });

    // close the dropdown when clicking outside
    document.addEventListener('click', function() {
        modeSwitcherMenu.classList.add('hidden');
    });
});
