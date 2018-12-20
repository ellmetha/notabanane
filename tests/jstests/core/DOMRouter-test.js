/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import DOMRouter from 'core/DOMRouter';


describe('DOMRouter', () => {
  test('can run a specific action of a specific controller', () => {
    const testController = { init: jest.fn() };
    const controllers = { test: testController };
    const router = new DOMRouter(controllers);
    router.execAction('test', 'init');
    expect(testController.init).toHaveBeenCalled();
  });

  test('can trigger the right controller using data attributes on the <body> tag', () => {
    const testController01 = {
      init: jest.fn(),
      doSomething: jest.fn(),
      doSomethingElse: jest.fn(),
    };
    const testController02 = { init: jest.fn(), doSomethingElseAgain: jest.fn() };
    const controllers = { test01: testController01, test02: testController02 };
    const router = new DOMRouter(controllers);
    // Set up our document body
    document.body.setAttribute('data-controller', 'test01');
    document.body.setAttribute('data-action', 'doSomething');
    router.init();
    expect(testController01.init).toHaveBeenCalled();
    expect(testController01.doSomething).toHaveBeenCalled();
    expect(testController01.doSomethingElse).not.toHaveBeenCalled();
    expect(testController02.init).not.toHaveBeenCalled();
    expect(testController02.doSomethingElseAgain).not.toHaveBeenCalled();
  });
});
