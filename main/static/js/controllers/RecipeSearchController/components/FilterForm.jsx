/* global gettext */

import {
  Formik,
  Field,
  FieldArray,
  Form,
} from 'formik';
import PropTypes from 'prop-types';
import React from 'react';

import CheckBox from '../../../core/components/forms/CheckBox';


const FilterForm = ({ onSubmitFilters }) => {
  const initialValues = {
    dishTypes: [],
    seasons: [],
  };

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

  return (
    <div id="recipe_filters_form">
      <Formik
        key="recipes-filter-form"
        initialValues={initialValues}
        onSubmit={(values) => {
          onSubmitFilters({ filters: values });
        }}
      >
        {({ values, setFieldValue, submitForm }) => (
          <Form>
            <h4 className="is-size-4">{gettext('Dish types')}</h4>
            <FieldArray
              name="dishTypes"
              render={arrayHelpers => (
                <div>
                  {filterableDishTypes.map(d => (
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
                              values.dishTypes.filter(el => el !== d[0]),
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
            <h4 className="is-size-4">{gettext('Seasons')}</h4>
            <FieldArray
              name="seasons"
              render={arrayHelpers => (
                <div>
                  {filterableSeasons.map(s => (
                    <div
                      key={`season-${s[0]}`}
                      className="form-check form-check-inline"
                    >
                      <Field
                        id={`dish_type_${s[0]}`}
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
                              values.seasons.filter(el => el !== s[0]),
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
