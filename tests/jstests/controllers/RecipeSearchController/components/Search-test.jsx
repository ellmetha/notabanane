/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import { act } from 'react-dom/test-utils';

import { MockedProvider } from '@apollo/react-testing';

import Search, { RECIPES } from 'controllers/RecipeSearchController/components/Search';


Enzyme.configure({ adapter: new Adapter() });

const mocks = [
  {
    request: {
      query: RECIPES,
      variables: {
        first: 10,
      },
    },
    result: {
      data: {
        recipes: {
          edges: [
            {
              id: 1,
              title: 'Test recipe',
              formattedDate: 'May 1, 2019',
              headerImageUrl: 'https://example.con/recipe-1/header.jpg',
              url: 'https://example.con/recipe-1',
            },
          ],
        },
      },
    },
  },
];

const waitForComponentToPaint = async (wrapper) => {
  await act(async () => {
    await new Promise(resolve => setTimeout(resolve, 0));
    wrapper.update();
  });
};

describe('<Search />', () => {
  beforeEach(() => {
    global.gettext = msgid => msgid;
  });

  test('can be properly rendered', () => {
    const component = Enzyme.mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <Search />
      </MockedProvider>
    );
    waitForComponentToPaint(component);
    expect(component.find('#recipe_search_engine').length).toEqual(1);
  });
});
