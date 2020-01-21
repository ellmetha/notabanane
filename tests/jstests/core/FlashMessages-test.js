/* eslint import/extensions: [0, {}] */
/* eslint import/first: 0 */
/* eslint import/no-unresolved: [0, {}] */

jest.mock('noty');
import Noty from 'noty';

import FlashMessages from 'core/FlashMessages';


describe('FlashMessages', () => {
  test('init() generates notification for each message', () => {
    document.body.innerHTML = '<div id="flash_messages">'
      + '  <div class="message" data-msg="This is the first test" data-type="success"></div>'
      + '  <div class="message" data-msg="This is the second test" data-type="danger"></div>'
      + '</div>';

    const mockedNoty = jest.fn();
    Noty.mockImplementation(mockedNoty);

    FlashMessages.init();

    expect(mockedNoty).toHaveBeenCalledTimes(2);

    expect(mockedNoty).toHaveBeenCalledWith({
      text: 'This is the first test',
      type: 'success',
      closeWith: ['click', 'button'],
      timeout: 10000,
      theme: 'sunset',
      layout: 'bottomRight',
    });

    expect(mockedNoty).toHaveBeenCalledWith({
      text: 'This is the second test',
      type: 'danger',
      closeWith: ['click', 'button'],
      timeout: 10000,
      theme: 'sunset',
      layout: 'bottomRight',
    });
  });
});
