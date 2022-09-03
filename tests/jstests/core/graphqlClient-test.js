/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import { ApolloClient } from '@apollo/client';

import graphqlClient from 'core/graphqlClient';

describe('graphqlClient', () => {
  test('is an Apollo client', () => {
    expect(graphqlClient).toBeInstanceOf(ApolloClient);
  });
});
