import React from 'react';
import ReactDOM from 'react-dom';

import { ApolloProvider } from '@apollo/react-hooks';

import graphqlClient from '../../core/graphqlClient';

import Search from './components/Search';


const SearchApp = () => (
  <ApolloProvider client={graphqlClient}>
    <Search />
  </ApolloProvider>
);

export default {
  init() {
    ReactDOM.render(<SearchApp />, document.getElementById('id_recipe_search_app'));
  },
};
