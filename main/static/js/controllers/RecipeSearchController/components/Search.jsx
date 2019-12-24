import { gql } from 'apollo-boost';
import React, { useState } from 'react';

import { useQuery } from '@apollo/react-hooks';

import smoothScrollTo from '../../../core/smoothScrollTo';

import FilterForm from './FilterForm';
import Pagination from './Pagination';
import ResultListItem from './ResultListItem';


const RECIPES = gql`
  query Recipes($first: Int, $cursor: String) {
    recipes(first: $first, after: $cursor) {
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
        hasPreviousPage
        hasNextPage
      }
      totalCount
    }
  }
`;

const RESULTS_PER_PAGE = 10;

const Search = () => {
  const [submitting, setSubmitting] = useState(false);
  const [cursorStack] = useState([]);

  const { data, fetchMore } = useQuery(RECIPES, { variables: { first: RESULTS_PER_PAGE } });
  const recipes = data ? data.recipes.edges.map(edge => edge.node) : [];
  const totalCount = data ? data.recipes.totalCount : null;
  const pageInfo = data ? data.recipes.pageInfo : null;

  const fetchRecipes = async (afterCursor) => {
    setSubmitting(true);
    await smoothScrollTo(document.documentElement);
    return fetchMore({
      variables: {
        first: RESULTS_PER_PAGE,
        cursor: afterCursor,
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        setSubmitting(false);
        return fetchMoreResult;
      },
    });
  };

  return (
    <div id="recipe_search_engine" className="section">
      <div className="container">
        <div className="columns is-multiline">
          <div id="search_filters" className="column is-one-third">
            <FilterForm
              onSubmitFilters={() => {

              }}
            />
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
            {pageInfo && (
              <Pagination
                hasPreviousPage={cursorStack.length > 0}
                hasNextPage={pageInfo.hasNextPage}
                onPaginatePrevious={() => {
                  cursorStack.pop();
                  return fetchRecipes(cursorStack[cursorStack.length - 1]);
                }}
                onPaginateNext={() => {
                  cursorStack.push(pageInfo.endCursor);
                  return fetchRecipes(pageInfo.endCursor);
                }}
                resultsPerPage={RESULTS_PER_PAGE}
                totalCount={totalCount}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Search;
