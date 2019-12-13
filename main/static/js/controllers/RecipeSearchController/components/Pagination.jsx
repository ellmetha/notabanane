import PropTypes from 'prop-types';
import React from 'react';


const Pagination = ({
  hasPreviousPage,
  hasNextPage,
  onPaginatePrevious,
  onPaginateNext,
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
      Previous
    </a>
    <a
      className="pagination-next"
      onClick={(ev) => {
        ev.preventDefault();
        if (hasNextPage) onPaginateNext();
      }}
      {...hasNextPage ? {} : { disabled: 'disabled' }}
    >
      Next page
    </a>
  </nav>
);

Pagination.propTypes = {
  hasPreviousPage: PropTypes.bool.isRequired,
  hasNextPage: PropTypes.bool.isRequired,
  onPaginatePrevious: PropTypes.func.isRequired,
  onPaginateNext: PropTypes.func.isRequired,
};

export default Pagination;
