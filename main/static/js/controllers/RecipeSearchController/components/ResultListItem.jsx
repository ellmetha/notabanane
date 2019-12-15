import PropTypes from 'prop-types';
import React from 'react';


const ResultListItem = ({ recipe }) => (
  <div className="column is-half">
    <a href={recipe.url} className="post-box" target="_blank" rel="noopener noreferrer">
      <span className="image-wrapper">
        <img alt={recipe.title} src={recipe.headerImageThumbnail} width="555" height="312" />
      </span>
      <span className="content-wrapper">
        <span className="post-date">{recipe.formattedDate}</span>
        <span className="post-title">{recipe.title}</span>
      </span>
    </a>
  </div>
);

ResultListItem.propTypes = {
  recipe: PropTypes.shape({
    title: PropTypes.string.isRequired,
    headerImageThumbnail: PropTypes.string.isRequired,
    formattedDate: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
  }).isRequired,
};

export default ResultListItem;
