/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import { act } from 'react-dom/test-utils'

import FilterForm from 'controllers/RecipeSearchController/components/FilterForm';


Enzyme.configure({ adapter: new Adapter() });

const waitForComponentToPaint = async (wrapper) => {
  await act(async () => {
    await new Promise(resolve => setTimeout(resolve, 0));
    wrapper.update();
  });
};

describe('<FilterForm />', () => {
  beforeEach(() => {
    global.gettext = (msgid) => msgid;
  });

  test('can be properly rendered', () => {
    const component = Enzyme.shallow(
      <FilterForm
        onSubmitFilters={jest.fn()}
      />
    );
    expect(component.find('#recipe_filters_form').length).toEqual(1);
  });

  test('calls the submit callback when the form is submitted', (done) => {
    const onSubmitFilters = (values) => {
      expect(values).toEqual({ dishTypes: ["APPETIZERS"], seasons: [] });
      done();
    };
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={onSubmitFilters}
      />
    );
    waitForComponentToPaint(component);
    component.find('input[value="APPETIZERS"]').simulate('change', { target: { checked: true } });
  });
});
