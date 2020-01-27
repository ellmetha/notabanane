import ApolloClient from 'apollo-boost';

import getCSRFToken from './getCSRFToken';
import reverseUrl from './reverseUrl';


const client = new ApolloClient({
  uri: reverseUrl('graphql'),
  headers: {
    'X-CSRFToken': getCSRFToken(),
  },
});

export default client;
