/* global gettext, interpolate, ngettext */

import PropTypes from 'prop-types';
import React from 'react';


const Pagination = ({
  hasPreviousPage,
  hasNextPage,
  onPaginatePrevious,
  onPaginateNext,
  resultsPerPage,
  totalCount,
}) => {
  let paginationText;

  if (hasPreviousPage || hasNextPage) {
    paginationText = interpolate(gettext('Showing %s of %s recipes'), [resultsPerPage, totalCount]);
  } else {
    paginationText = interpolate(
      ngettext('Showing %s recipe', 'Showing %s recipes', resultsPerPage),
      [resultsPerPage],
    );
  }

  return (
    <nav
      role="navigation"
      aria-label="pagination"
      {...(hasPreviousPage || hasNextPage)
        ? { className: 'pagination' }
        : { className: 'pagination no-direction-available' }
      }
    >
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
      <div className="pagination-list">{paginationText}</div>
    </nav>
  );
};

Pagination.propTypes = {
  hasPreviousPage: PropTypes.bool.isRequired,
  hasNextPage: PropTypes.bool.isRequired,
  onPaginatePrevious: PropTypes.func.isRequired,
  onPaginateNext: PropTypes.func.isRequired,
  resultsPerPage: PropTypes.number.isRequired,
  totalCount: PropTypes.number.isRequired,
};

export default Pagination;
