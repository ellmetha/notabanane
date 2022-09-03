import { ApolloClient, HttpLink, InMemoryCache } from '@apollo/client';
import fetch from 'cross-fetch';

import getCSRFToken from './getCSRFToken';
import reverseUrl from './reverseUrl';

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: new HttpLink({
    uri: reverseUrl('graphql'),
    headers: {
      'X-CSRFToken': getCSRFToken(),
    },
    fetch,
  }),
});

export default client;
