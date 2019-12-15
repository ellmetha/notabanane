/* global gettext, interpolate */

import PropTypes from 'prop-types';
import React from 'react';


const Pagination = ({
  hasPreviousPage,
  hasNextPage,
  onPaginatePrevious,
  onPaginateNext,
  resultsPerPage,
  totalCount,
}) => (
  <nav className="pagination" role="navigation" aria-label="pagination">
    <a
      className="pagination-previous"
      onClick={(ev) => {
        ev.preventDefault();
        if (hasPreviousPage) onPaginatePrevious();
      }}
      {...hasPreviousPage ? {} : { disabled: 'disabled' }}
    >
      <i className="fa fa-angle-left" />
    </a>
    <a
      className="pagination-next"
      onClick={(ev) => {
        ev.preventDefault();
        if (hasNextPage) onPaginateNext();
      }}
      {...hasNextPage ? {} : { disabled: 'disabled' }}
    >
      <i className="fa fa-angle-right" />
    </a>
    <div className="pagination-list">
      {interpolate(gettext('Showing %s of %s recipes'), [resultsPerPage, totalCount])}
    </div>
  </nav>
);

Pagination.propTypes = {
  hasPreviousPage: PropTypes.bool.isRequired,
  hasNextPage: PropTypes.bool.isRequired,
  onPaginatePrevious: PropTypes.func.isRequired,
  onPaginateNext: PropTypes.func.isRequired,
  resultsPerPage: PropTypes.number.isRequired,
  totalCount: PropTypes.number.isRequired,
};

export default Pagination;
