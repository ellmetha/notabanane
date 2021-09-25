import { createBrowserHistory, createMemoryHistory } from 'history';

const isTest = process.env.NODE_ENV === 'test';
export default isTest ? createMemoryHistory() : createBrowserHistory();
