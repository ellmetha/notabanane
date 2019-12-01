import ApolloClient from 'apollo-boost';

import React from 'react';
import ReactDOM from 'react-dom';

import { ApolloProvider } from '@apollo/react-hooks';

import getCSRFToken from '../../core/getCSRFToken';

import Search from './components/Search';


const client = new ApolloClient({
  uri: 'http://127.0.0.1:8000/graphql/',
  headers: {
    'X-CSRFToken': getCSRFToken(),
  },
});

const SearchApp = () => (
  <ApolloProvider client={client}>
    <Search />
  </ApolloProvider>
);

export default {
  init() {
    ReactDOM.render(<SearchApp />, document.getElementById('id_recipe_search_app'));
  },
};
