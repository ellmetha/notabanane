/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';

import Pagination from 'controllers/RecipeSearchController/components/Pagination';


Enzyme.configure({ adapter: new Adapter() });


describe('<Pagination />', () => {
  beforeEach(() => {
    global.gettext = msgid => msgid;
    global.ngettext = (singular, plural, count) => (
      (count === 1) ? singular : plural
    );
    global.interpolate = (fmt, obj, named) => {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, match => String(obj[match.slice(2, -2)]));
      }
      return fmt.replace(/%s/g, () => String(obj.shift()));
    };
  });

  test('disables the previous button if no previous page is available', () => {
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={false}
        hasNextPage={true}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={jest.fn()}
        resultsPerPage={10}
        totalCount={100}
      />
    );
    expect(component.find('.pagination-previous').prop('disabled')).toEqual('disabled');
  });

  test('disables the next button if no next page is available', () => {
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={true}
        hasNextPage={false}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={jest.fn()}
        resultsPerPage={10}
        totalCount={100}
      />
    );
    expect(component.find('.pagination-next').prop('disabled')).toEqual('disabled');
  });

  test('triggers pagination from the "previous" button', () => {
    const onPaginatePrevious = jest.fn();
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={true}
        hasNextPage={false}
        onPaginatePrevious={onPaginatePrevious}
        onPaginateNext={jest.fn()}
        resultsPerPage={10}
        totalCount={100}
      />
    );
    component.find('.pagination-previous').simulate('click', { preventDefault: jest.fn() });
    expect(onPaginatePrevious).toHaveBeenCalled();
  });

  test('triggers pagination from the "next" button', () => {
    const onPaginateNext = jest.fn();
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={false}
        hasNextPage={true}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={onPaginateNext}
        resultsPerPage={10}
        totalCount={100}
      />
    );
    component.find('.pagination-next').simulate('click', { preventDefault: jest.fn() });
    expect(onPaginateNext).toHaveBeenCalled();
  });

  test('adds a special class to the nav tag if no directional page is available', () => {
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={false}
        hasNextPage={false}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={jest.fn()}
        resultsPerPage={4}
        totalCount={4}
      />
    );
    expect(component.find('.pagination').hasClass('no-direction-available')).toBeTruthy();
  });

  test('displays the right text when the number of results per page is greater than 1', () => {
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={false}
        hasNextPage={true}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={jest.fn()}
        resultsPerPage={10}
        totalCount={100}
      />
    );
    expect(component.find('.pagination-list').text()).toEqual('Showing 10 of 100 recipes');
  });

  test('displays the right text when the number of results per page is 1', () => {
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={true}
        hasNextPage={false}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={jest.fn()}
        resultsPerPage={1}
        totalCount={100}
      />
    );
    expect(component.find('.pagination-list').text()).toEqual('Showing 1 of 100 recipes');
  });

  test('displays the appropriate text when no directional pages are available', () => {
    const component = Enzyme.shallow(
      <Pagination
        key="pagination"
        hasPreviousPage={false}
        hasNextPage={false}
        onPaginatePrevious={jest.fn()}
        onPaginateNext={jest.fn()}
        resultsPerPage={4}
        totalCount={4}
      />
    );
    expect(component.find('.pagination-list').text()).toEqual('Showing 4 recipes');
  });
});
