/* global gettext */

import { gql } from 'apollo-boost';
import React, { useEffect, useRef, useState } from 'react';

import { useQuery } from '@apollo/react-hooks';

import smoothScrollTo from '../../../core/smoothScrollTo';

import getInitialFilters from '../utilities/getInitialFilters';

import FilterForm from './FilterForm';
import Pagination from './Pagination';
import ResultListItem from './ResultListItem';

export const RECIPES = gql`
  query Recipes(
    $first: Int,
    $cursor: String,
    $dishTypes: [String],
    $seasons: [String],
    $diets: [String]
  ) {
    recipes(
      first: $first,
      after: $cursor,
      dishTypes: $dishTypes,
      seasons: $seasons,
      diets: $diets
    ) {
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
  const [showMobileFilters, setShowMobileFilters] = useState(false);
  const [cursorStack] = useState([]);
  const [currentFilters, setCurrentFilters] = useState({});

  const searchEngineNode = useRef(null);
  const toggleMobileFiltersWrapperNode = useRef(null);

  const initialFilters = getInitialFilters();

  const { data, fetchMore, loading } = useQuery(
    RECIPES,
    { variables: { first: RESULTS_PER_PAGE, ...initialFilters }, fetchPolicy: 'network-only' },
  );
  const recipes = data ? data.recipes.edges.map((edge) => edge.node) : [];
  const totalCount = data ? data.recipes.totalCount : null;
  const pageInfo = data ? data.recipes.pageInfo : null;

  const filterLabel = gettext('Filters');
  const viewResultsLabel = gettext('View recipes');
  const noResultsTitle = gettext('No results');
  const noResultsDescription = gettext('To get more results, try changing your filters.');

  useEffect(() => {
    if (!loading) {
      toggleMobileFiltersWrapperNode.current.scrollIntoView();
    }
  }, [showMobileFilters]);

  const fetchRecipes = async ({ filters = null, direction = null }) => {
    setSubmitting(true);

    if (filters != null) {
      setCurrentFilters(filters);
    }

    if (!showMobileFilters) {
      await smoothScrollTo(
        document.documentElement,
        searchEngineNode.current.offsetTop + toggleMobileFiltersWrapperNode.current.offsetTop,
        200,
      );
    }

    // Updates the after cursor and the stack of cursors depending on the direction of the
    // pagination (if the results are paginated).
    let afterCursor = null;
    if (direction === 'previous') {
      cursorStack.pop();
      afterCursor = cursorStack[cursorStack.length - 1];
    } else if (direction === 'next') {
      cursorStack.push(pageInfo.endCursor);
      afterCursor = pageInfo.endCursor;
    }

    return fetchMore({
      variables: {
        first: RESULTS_PER_PAGE,
        cursor: afterCursor,
        ...(filters || currentFilters),
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        setSubmitting(false);
        return fetchMoreResult;
      },
    });
  };

  const onPaginatePrevious = () => (
    fetchRecipes({ direction: 'previous' })
  );

  const onPaginateNext = () => (
    fetchRecipes({ direction: 'next' })
  );

  return (
    <div
      id="recipe_search_engine"
      ref={searchEngineNode}
      className={`section ${showMobileFilters ? 'filters-on' : ''}`}
    >
      <div
        id="toggle_mobile_filters_wrapper"
        ref={toggleMobileFiltersWrapperNode}
        className="is-hidden-tablet"
      >
        <button
          type="button"
          className="button is-primary"
          onClick={() => {
            setShowMobileFilters(!showMobileFilters);
          }}
        >
          {showMobileFilters === true && (
            <span>{viewResultsLabel}</span>
          )}
          {showMobileFilters === false && (
            <span>
              <i className="fa fa-filter" aria-hidden="true" />
              {filterLabel}
            </span>
          )}
        </button>
      </div>
      <div className="container">
        <div className="columns is-multiline">
          <div id="search_filters" className="column is-one-third">
            <FilterForm
              onSubmitFilters={(values) => {
                cursorStack.length = 0;
                fetchRecipes({ filters: values });
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
            {pageInfo && recipes.length > 0 && (
              <Pagination
                hasPreviousPage={cursorStack.length > 0}
                hasNextPage={pageInfo.hasNextPage}
                onPaginatePrevious={onPaginatePrevious}
                onPaginateNext={onPaginateNext}
                resultsPerPage={recipes.length}
                totalCount={totalCount}
              />
            )}
            {recipes.length > 0 && (
              <div className="columns is-multiline post-list">
                {recipes.map((recipe) => (
                  <ResultListItem
                    key={recipe.id}
                    recipe={recipe}
                  />
                ))}
              </div>
            )}
            {recipes.length === 0 && !submitting && !loading && (
              <div id="search_results_empty">
                <h3 className="is-size-3">{noResultsTitle}</h3>
                <p>{noResultsDescription}</p>
              </div>
            )}
            {pageInfo && recipes.length > 0 && (
              <Pagination
                hasPreviousPage={cursorStack.length > 0}
                hasNextPage={pageInfo.hasNextPage}
                onPaginatePrevious={onPaginatePrevious}
                onPaginateNext={onPaginateNext}
                resultsPerPage={recipes.length}
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
