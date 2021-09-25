/**
 * @jest-environment jsdom
 */

/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import Enzyme from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import React from 'react';

import ResultListItem from 'controllers/RecipeSearchController/components/ResultListItem';

Enzyme.configure({ adapter: new Adapter() });

describe('<ResultListItem />', () => {
  test('can be properly rendered', () => {
    const recipe = {
      title: 'Cold soup',
      url: 'https://example.com/cold-soup',
      headerImageThumbnail: 'https://example.com/static-images/cold-soup.jpg',
      formattedDate: 'Dec. 27 2019',
    };

    const component = Enzyme.shallow(
      <ResultListItem
        recipe={recipe}
      />
    );
    expect(component.find('.post-title').text()).toEqual(recipe.title);
  });
});
