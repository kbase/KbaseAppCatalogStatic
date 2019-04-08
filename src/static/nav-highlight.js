// Highlight sidebar nav items based on the current scroll position.

// Number of category nav items on the page
const numCategories = document.getElementById('organized_list_items');
const num = Number(numCategories.dataset.name);

let currentElem = 1;

// Find and highlight the currently scrolled section
const findHiddenElem = () => {
  let elemIndex = 0;
  for (let i = 0; i < num; i += 1) {
    const elem = document.getElementsByClassName('organized-by')[i]
        .getBoundingClientRect();
    if (elem.top < 60) {
      elemIndex += 1;
    }
  }
  elemIndex += 1;
  if (currentElem !== elemIndex) {
    document.body
        .querySelector('.table tbody tr:nth-child(' + currentElem + ') a')
        .removeAttribute('style');
  }
  document.body
      .querySelector('.table tbody tr:nth-child(' + elemIndex + ') a')
      .setAttribute('style', 'color: #576523; font-weight: bold;');
  currentElem = elemIndex;
};

// Run the callback `callback` at most every `delayMs` milliseconds
const debounce = (delayMs, callback) => {
  let timeout;
  return function() {
    const args = arguments;
    const later = () => {
      timeout = null;
      callback.apply(null, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, delayMs);
  };
};


// On pageload and on scroll (with a 100ms delay), find the current section the
// user has scrolled to and highlight that in the navigation sidebar
findHiddenElem();
window.addEventListener('scroll', debounce(10, findHiddenElem));
