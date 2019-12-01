import cookie from './cookie';


export default function getCSRFToken() {
  return cookie.get('csrftoken');
}
