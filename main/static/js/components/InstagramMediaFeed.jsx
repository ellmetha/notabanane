import { gql } from 'apollo-boost';
import React from 'react';

import { useQuery } from '@apollo/react-hooks';

export const INSTAGRAM_MEDIA_FEED = gql`
  {
    recentInstagramMedias {
      url
      imageUrl
    }
  }
`;

const InstagramMediaFeed = () => {
  const { data } = useQuery(INSTAGRAM_MEDIA_FEED);
  const medias = data ? data.recentInstagramMedias : [];

  return (
    <div id="instagram_media_feed">
      <div className="columns is-vcentered is-multiline is-variable is-3 is-mobile">
        {medias.map((media) => (
          <a
            href={media.url}
            key={media.url}
            className="column is-one-quarter-desktop is-one-third-tablet is-half-mobile"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src={media.imageUrl} alt="" />
          </a>
        ))}
      </div>
    </div>
  );
};

export default InstagramMediaFeed;
