/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import Cookies from 'js-cookie';

import getCSRFToken from 'core/getCSRFToken';

describe('getCSRFToken', () => {
  test('returns the CSRF token from the corresponding cookie', () => {
    const spy = jest.spyOn(Cookies, 'get');
    getCSRFToken();
    expect(spy).toHaveBeenCalledWith('csrftoken');
  });
});
