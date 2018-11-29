/* eslint-env browser */
import 'regenerator-runtime/runtime';

import controllers from './controllers';
import DOMRouter from './core/DOMRouter';


const router = new DOMRouter(controllers);

document.addEventListener('DOMContentLoaded', () => {
  // Initializes the DOM router. The DOM router is used to execute specific portions of JS code for
  // each specific page.
  router.init();

  // Initializes the navbar behaviours; which should be visible on every page of the webapp.
  const navBarSearchInputContainer = document.querySelector('#search_input_container');
  const navBarSearchInput = document.querySelector('#search_input_container input');
  const navBarSearchForm = document.querySelector('#search_input_container form');
  document.querySelector('#search_toggler_wrapper a').addEventListener('click', () => {
    if (navBarSearchInputContainer.classList.contains('on')) {
      // The search form is visible.
      if (!navBarSearchInput.value) {
        navBarSearchInputContainer.classList.remove('on');
      } else {
        navBarSearchForm.submit();
      }
    } else {
      // The search form is hidden.
      navBarSearchInputContainer.classList.add('on');
      navBarSearchInput.focus();
    }
  });
  document.addEventListener('click', (ev) => {
    if (!ev.target.closest('#search_input_container')
        && !ev.target.closest('#search_toggler_wrapper')
        && navBarSearchInputContainer.classList.contains('on')) {
      navBarSearchInputContainer.classList.remove('on');
      navBarSearchInput.value = '';
    }
  });
});
