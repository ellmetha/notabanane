/**
 * @jest-environment jsdom
 */

/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import Enzyme from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import React from 'react';
import { act } from 'react-dom/test-utils';

import FilterForm from 'controllers/RecipeSearchController/components/FilterForm';

Enzyme.configure({ adapter: new Adapter() });

const waitForComponentToPaint = async (wrapper) => {
  await act(async () => {
    await new Promise((resolve) => setTimeout(resolve, 0));
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

  test('properly updates dish type checkboxes when they are checked', (done) => {
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={(values) => {
          expect(values.dishTypes).toEqual(['APPETIZERS']);
          done();
        }}
      />
    );
    waitForComponentToPaint(component);
    component.find('input[value="APPETIZERS"]').simulate('change', { target: { checked: true } });
  });

  test('properly updates dish type checkboxes when they are unchecked', (done) => {
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={(values) => {
          expect(values.dishTypes).toEqual(['APPETIZERS']);
          done();
        }}
      />
    );

    component.setProps({
      onSubmitFilters: (values) => {
        expect(values.dishTypes).toEqual([]);
        done();
      },
    });
    waitForComponentToPaint(component);

    component.find('input[value="APPETIZERS"]').simulate('change', { target: { checked: false } });
  });

  test('properly updates season checkboxes when they are checked', (done) => {
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={(values) => {
          expect(values.seasons).toEqual(['WINTER']);
          done();
        }}
      />
    );
    waitForComponentToPaint(component);
    component.find('input[value="WINTER"]').simulate('change', { target: { checked: true } });
  });

  test('properly updates season checkboxes when they are unchecked', (done) => {
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={(values) => {
          expect(values.seasons).toEqual(['WINTER']);
          done();
        }}
      />
    );

    component.setProps({
      onSubmitFilters: (values) => {
        expect(values.seasons).toEqual([]);
        done();
      },
    });
    waitForComponentToPaint(component);

    component.find('input[value="WINTER"]').simulate('change', { target: { checked: false } });
  });

  test('properly updates diet checkboxes when they are checked', (done) => {
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={(values) => {
          expect(values.diets).toEqual(['VEGETARIAN']);
          done();
        }}
      />
    );
    waitForComponentToPaint(component);
    component.find('input[value="VEGETARIAN"]').simulate('change', { target: { checked: true } });
  });

  test('properly updates diet checkboxes when they are unchecked', (done) => {
    const component = Enzyme.mount(
      <FilterForm
        onSubmitFilters={(values) => {
          expect(values.diets).toEqual(['VEGETARIAN']);
          done();
        }}
      />
    );

    component.setProps({
      onSubmitFilters: (values) => {
        expect(values.diets).toEqual([]);
        done();
      },
    });
    waitForComponentToPaint(component);

    component.find('input[value="VEGETARIAN"]').simulate('change', { target: { checked: false } });
  });
});
