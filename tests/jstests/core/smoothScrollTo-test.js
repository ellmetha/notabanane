/* eslint comma-dangle: 0 */
/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import smoothScrollTo from 'core/smoothScrollTo';


describe('smoothScrollTo()', () => {
  test('scrolls to a specific element', async () => {
    document.documentElement.scrollTop = 15;
    await smoothScrollTo(document.documentElement);
    expect(document.documentElement.scrollTop).toEqual(0);
  });
});
