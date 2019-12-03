import { gql } from 'apollo-boost';
import React, { useState } from 'react';

import { useQuery } from '@apollo/react-hooks';

import ResultListItem from './ResultListItem';


const RECIPES = gql`
  query Recipes($cursor: String) {
    recipes(first: 10, after: $cursor) {
      edges {
        node {
          id
          title
          formattedDate
          headerImageThumbnail
          url
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`;

const Search = () => {
  const [submitting, setSubmitting] = useState(false);

  const { data, loading } = useQuery(RECIPES);
  const recipes = data ? data.recipes.edges.map(edge => edge.node) : [];

  if (submitting !== loading) {
    setSubmitting(loading);
  }

  return (
    <div id="recipe_search_engine" className="section">
      <div className="container">
        <div className="columns is-multiline">
          <div id="search_filters" className="column is-one-third">
            FILTERS
          </div>
          <div
            id="search_results"
            {...submitting
              ? { className: 'fetching column is-two-thirds' }
              : { className: 'column is-two-thirds' }
            }
          >
            <div id="search_results_fetching" />
            {recipes.length > 0 && (
              <div className="columns is-multiline post-list">
                {recipes.map(recipe => (
                  <ResultListItem
                    key={recipe.id}
                    recipe={recipe}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Search;
