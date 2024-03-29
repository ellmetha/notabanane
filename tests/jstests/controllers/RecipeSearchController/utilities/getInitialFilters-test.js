/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import queryString from 'query-string';

import getInitialFilters from 'controllers/RecipeSearchController/utilities/getInitialFilters';
import history from 'core/history';

describe('getInitialFilters()', () => {
  test('extracts dish types values from the history', () => {
    history.push({
      location: '/',
      search: queryString.stringify({ dishTypes: ['APPETIZERS', 'SOUPS'] }),
    });
    expect(getInitialFilters()).toEqual(
      { dishTypes: ['APPETIZERS', 'SOUPS'], seasons: [], diets: [] }
    );
  });

  test('extracts seasons values from the history', () => {
    history.push({
      location: '/',
      search: queryString.stringify({ seasons: ['WINTER', 'SPRING'] }),
    });
    expect(getInitialFilters()).toEqual(
      { dishTypes: [], seasons: ['WINTER', 'SPRING'], diets: [] }
    );
  });

  test('extracts diets values from the history', () => {
    history.push({
      location: '/',
      search: queryString.stringify({ seasons: ['VEGAN', 'VEGETARIAN'] }),
    });
    expect(getInitialFilters()).toEqual(
      { diets: [], dishTypes: [], seasons: ['VEGAN', 'VEGETARIAN'] }
    );
  });
});
