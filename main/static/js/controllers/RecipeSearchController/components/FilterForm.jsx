/* global gettext */

import {
  Formik,
  Field,
  FieldArray,
  Form,
} from 'formik';
import PropTypes from 'prop-types';
import queryString from 'query-string';
import React from 'react';

import CheckBox from '../../../core/components/forms/CheckBox';
import history from '../../../core/history';
import getInitialFilters from '../utilities/getInitialFilters';

const FilterForm = ({ onSubmitFilters }) => {
  const initialValues = getInitialFilters();

  const filterableDishTypes = [
    ['APPETIZERS', gettext('Appetizers')],
    ['BEVERAGES', gettext('Beverages')],
    ['BREAKFAST', gettext('Breakfast')],
    ['DESSERTS', gettext('Desserts')],
    ['MAIN_COURSE', gettext('Main course')],
    ['SAUCES_SALAD_DRESSINGS', gettext('Sauces and salad dressings')],
    ['SOUPS', gettext('Soups')],
    ['VEGETABLES_SALADS', gettext('Vegetables and salads')],
  ];

  const filterableSeasons = [
    ['WINTER', gettext('Winter')],
    ['SPRING', gettext('Spring')],
    ['SUMMER', gettext('Summer')],
    ['AUTUMN', gettext('Autumn')],
  ];

  const filterableDiets = [
    ['VEGETARIAN', gettext('Vegetarian')],
    ['VEGAN', gettext('Vegan')],
    ['GLUTEN_FREE', gettext('Gluten free')],
    ['LACTOSE_FREE', gettext('Lactose free')],
  ];

  const dishTypesFilterLabel = gettext('Dish types');
  const seasonsFilterLabel = gettext('Seasons');
  const dietsFilterLabel = gettext('Diets');

  return (
    <div id="recipe_filters_form">
      <Formik
        key="recipes-filter-form"
        initialValues={initialValues}
        onSubmit={(values) => {
          // Pushes the querystring to the browser history.
          history.push({ ...history.location, search: queryString.stringify(values) });
          // Submit the filters.
          onSubmitFilters(values);
        }}
      >
        {({ values, setFieldValue, submitForm }) => (
          <Form>
            <h4 className="is-size-4">{dishTypesFilterLabel}</h4>
            <FieldArray
              name="dishTypes"
              render={(arrayHelpers) => (
                <div>
                  {filterableDishTypes.map((d) => (
                    <div
                      key={`dish-type-${d[0]}`}
                      className="form-check form-check-inline"
                    >
                      <Field
                        id={`dish_type_${d[0]}`}
                        name="dishTypes"
                        value={d[0]}
                        checked={values.dishTypes ? values.dishTypes.includes(d[0]) : false}
                        label={d[1]}
                        component={CheckBox}
                        onChange={(e) => {
                          if (e.target.checked) {
                            arrayHelpers.push(d[0]);
                          } else {
                            setFieldValue(
                              'dishTypes',
                              values.dishTypes.filter((el) => el !== d[0]),
                            );
                          }
                          submitForm();
                        }}
                      />
                    </div>
                  ))}
                </div>
              )}
            />
            <h4 className="is-size-4">{seasonsFilterLabel}</h4>
            <FieldArray
              name="seasons"
              render={(arrayHelpers) => (
                <div>
                  {filterableSeasons.map((s) => (
                    <div
                      key={`season-${s[0]}`}
                      className="form-check form-check-inline"
                    >
                      <Field
                        id={`season_${s[0]}`}
                        name="seasons"
                        value={s[0]}
                        checked={values.seasons ? values.seasons.includes(s[0]) : false}
                        label={s[1]}
                        component={CheckBox}
                        onChange={(e) => {
                          if (e.target.checked) {
                            arrayHelpers.push(s[0]);
                          } else {
                            setFieldValue(
                              'seasons',
                              values.seasons.filter((el) => el !== s[0]),
                            );
                          }
                          submitForm();
                        }}
                      />
                    </div>
                  ))}
                </div>
              )}
            />
            <h4 className="is-size-4">{dietsFilterLabel}</h4>
            <FieldArray
              name="diets"
              render={(arrayHelpers) => (
                <div>
                  {filterableDiets.map((s) => (
                    <div
                      key={`diet-${s[0]}`}
                      className="form-check form-check-inline"
                    >
                      <Field
                        id={`diet_${s[0]}`}
                        name="diets"
                        value={s[0]}
                        checked={values.diets ? values.diets.includes(s[0]) : false}
                        label={s[1]}
                        component={CheckBox}
                        onChange={(e) => {
                          if (e.target.checked) {
                            arrayHelpers.push(s[0]);
                          } else {
                            setFieldValue(
                              'diets',
                              values.diets.filter((el) => el !== s[0]),
                            );
                          }
                          submitForm();
                        }}
                      />
                    </div>
                  ))}
                </div>
              )}
            />
          </Form>
        )}
      </Formik>
    </div>
  );
};

FilterForm.propTypes = {
  onSubmitFilters: PropTypes.func.isRequired,
};

export default FilterForm;
