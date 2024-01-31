////////////////////////////////////////////////////////////////////////////////////////////////////
// Controls toggling the icon in the navbar and the color theme of all pages.
// In the <HTML> element tag it changes the 'data-bs-theme' to light or dark,
// utilizing Bootstraps built in color modes to change themes on components globally.
// Script is loaded in the <head> to avoid unstyled content flashing on page load.
// Adapted from Bootstrap's Color Modes https://getbootstrap.com/docs/5.3/customize/color-modes/
////////////////////////////////////////////////////////////////////////////////////////////////////
(function () {
  const getStoredTheme = () => localStorage.getItem('theme');
  const setStoredTheme = theme => localStorage.setItem('theme', theme);


  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if(storedTheme) {
      return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };


  const setTheme = theme => {
    if(window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-bs-theme', 'dark')
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  };


  // Set light or dark in initial script load.
  setTheme(getPreferredTheme());


  const showActiveThemeIcon = (theme) => {
    const themeSwitcherIcon = document.getElementById('bd-theme') // Theme icon button
    const icons = ['bi-sun', 'black', 'bi-moon', 'white']

    if(!themeSwitcherIcon) {
      return;
    }

    const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)

    document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
      element.classList.remove('active')
      element.setAttribute('aria-pressed', 'false')
    });

    btnToActive.classList.add('active')
    btnToActive.setAttribute('aria-pressed', 'true')

    themeSwitcherIcon.classList.remove(icons[0])
    themeSwitcherIcon.classList.remove(icons[2])
    if(theme === 'light') {
      themeSwitcherIcon.classList.add(icons[0])
      themeSwitcherIcon.style.color = icons[1]
    } else {
      themeSwitcherIcon.classList.add(icons[2])
      themeSwitcherIcon.style.color = icons[3]
    }
  };


  // After initial page load display correct icon in navbar.
  window.addEventListener('DOMContentLoaded', () => {
    showActiveThemeIcon(getPreferredTheme());

    // When icon is toggled, change theme and icon.
    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(toggle => {
        toggle.addEventListener('click', () => {
          const theme = toggle.getAttribute('data-bs-theme-value')
          setStoredTheme(theme);
          setTheme(theme);
          showActiveThemeIcon(theme);
        });
      });
  });
})()
