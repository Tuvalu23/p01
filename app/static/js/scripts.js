// finction to set the user mode
function setMode(mode) {
    // remove existing mode
    document.body.classList.remove('light-mode', 'dark-mode', 'topher-mode');

    // add selected mode
    document.body.classList.add(mode + '-mode');

    // save
    localStorage.setItem('mode', mode);

    // update navbar and footer
    const navbar = document.querySelector('.navbar');
    const footer = document.querySelector('.footer');
    navbar.classList.remove('light-mode', 'dark-mode', 'topher-mode');
    footer.classList.remove('light-mode', 'dark-mode', 'topher-mode');
    navbar.classList.add(mode + '-mode');
    footer.classList.add(mode + '-mode');
}

// function to save mode on page
function loadMode() {
    const savedMode = localStorage.getItem('mode') || 'light';
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
