import queryString from 'query-string';

import history from '../../../core/history';

export default function getInitialFilters() {
  const initialParameters = queryString.parse(history.location.search);
  return {
    dishTypes: initialParameters.dishTypes
      ? [initialParameters.dishTypes].reduce((acc, val) => acc.concat(val), [])
      : [],
    seasons: initialParameters.seasons
      ? [initialParameters.seasons].reduce((acc, val) => acc.concat(val), [])
      : [],
    diets: initialParameters.diets
      ? [initialParameters.diets].reduce((acc, val) => acc.concat(val), [])
      : [],
  };
}
