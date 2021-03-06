import ApolloClient from 'apollo-boost';
import fetch from 'unfetch';

import getCSRFToken from './getCSRFToken';
import reverseUrl from './reverseUrl';


const client = new ApolloClient({
  uri: reverseUrl('graphql'),
  headers: {
    'X-CSRFToken': getCSRFToken(),
  },
  fetch,
});

export default client;
