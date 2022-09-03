/* eslint-env browser */
import 'core-js/stable';
import 'regenerator-runtime/runtime';

import feather from 'feather-icons/dist/feather';
import React from 'react';
import ReactDOM from 'react-dom';

import { ApolloProvider } from '@apollo/client';

import InstagramMediaFeed from './components/InstagramMediaFeed';
import controllers from './controllers';
import DOMRouter from './core/DOMRouter';
import FlashMessages from './core/FlashMessages';
import graphqlClient from './core/graphqlClient';


const router = new DOMRouter(controllers);

document.addEventListener('DOMContentLoaded', () => {
  // Initializes feather icons.
  feather.replace();

  // Initializes the DOM router. The DOM router is used to execute specific portions of JS code for
  // each specific page.
  router.init();

  // Initializes flash messages.
  FlashMessages.init();

  // Initializes the navbar behaviours; which should be visible on every page of the webapp.
  const navBarSearchTogglerButton = document.querySelector('#search_toggler_wrapper a');
  const navBarSearchInputContainer = document.querySelector('#search_input_container');
  const navBarSearchInput = document.querySelector('#search_input_container input');
  const navBarSearchForm = document.querySelector('#search_input_container form');
  navBarSearchTogglerButton.addEventListener('click', () => {
    if (navBarSearchInputContainer.classList.contains('on')) {
      // The search form is visible.
      if (!navBarSearchInput.value) {
        navBarSearchTogglerButton.classList.remove('on');
        navBarSearchInputContainer.classList.remove('on');
      } else {
        navBarSearchForm.submit();
      }
    } else {
      // The search form is hidden.
      navBarSearchTogglerButton.classList.add('on');
      navBarSearchInputContainer.classList.add('on');
      navBarSearchInput.focus();
    }
  });
  document.addEventListener('click', (ev) => {
    if (!ev.target.closest('#search_input_container')
        && !ev.target.closest('#search_toggler_wrapper')
        && navBarSearchInputContainer.classList.contains('on')) {
      navBarSearchTogglerButton.classList.remove('on');
      navBarSearchInputContainer.classList.remove('on');
      navBarSearchInput.value = '';
    }
  });

  // Initializes responsive-specific behaviours.
  const largeDevicesWidth = 1025;
  const navBarMenu = document.getElementById('notabanane_navbar');
  const navBarToggler = document.querySelector('.navbar-burger');

  function toggleAction(ev) {
    ev.stopImmediatePropagation();
    navBarMenu.classList.toggle('opened');
    document.body.classList.toggle('navbar-menu-opened');
    navBarToggler.classList.toggle('is-active');
  }

  function closeNavBar(ev) {
    ev.stopImmediatePropagation();
    if (!ev.target.closest('.navbar-toggler, #notabanane_navbar')) {
      navBarMenu.classList.remove('opened');
      document.body.classList.remove('navbar-menu-opened');
      navBarToggler.classList.remove('is-active');
    }
  }

  window.addEventListener('resize', () => {
    if (window.innerWidth <= largeDevicesWidth) {
      navBarToggler.addEventListener('click', ev => toggleAction(ev));
      document.addEventListener('click', ev => closeNavBar(ev));
    }
  });
  window.dispatchEvent(new Event('resize'));

  // Initialies the Instagram media feed.
  ReactDOM.render(
    <ApolloProvider client={graphqlClient}>
      <InstagramMediaFeed />
    </ApolloProvider>,
    document.getElementById('instagram_media_feed_wrapper')
  );
});
