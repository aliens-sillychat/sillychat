const WS_ENDPOINT = 'ws://sillychat.kro.kr/api/ws';

/**
 * @typedef {{ id: string, name: string }} User
 */

/**
 * @typedef {(
 *   { type: 'join', user: User }
 *   | { type: 'leave', user: User }
 *   | { type: 'message', user: User, content: string, blurWord?: string }
 *   | { type: 'ban', user: User, reason: string }
 * )} Message
 */

/** @type {null|WebSocket} */
let ws = null;

function uuidv4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
  );
}

function createElement(html) {
  const template = document.createElement('template');
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
}

/**
 * @param {string} username
 */
function setUser(username = null) {
  const user = getUser();

  localStorage.setItem(
    'user',
    JSON.stringify({
      id: user?.id ?? uuidv4(),
      name: username,
    })
  );
}

/**
 * @returns {User}
 */
function getUser() {
  const serializedUser = localStorage.getItem('user');
  if (serializedUser === null) return null;
  return JSON.parse(serializedUser);
}

function resetUser() {
  localStorage.removeItem('user');
  setUser();
  return getUser();
}

/**
 * @param {string} message
 */
function sendMessage(content) {
  const message = {
    type: 'message',
    user: getUser(),
    content,
  };
  ws?.send(JSON.stringify(message));
}

function sendJoin() {
  const message = {
    type: 'join',
    user: getUser(),
  };
  ws?.send(JSON.stringify(message));
}

function connect() {
  if (ws !== null) {
    console.warn('You are already connected!');
    return;
  }

  ws = new WebSocket(WS_ENDPOINT);

  ws.onopen = function () {
    console.log('onConnectionOpen');
    onConnectionOpen?.();
    sendJoin();
  };
  ws.onerror = function () {
    console.log('onConnectionError');
    onConnectionError?.();
  };
  ws.onclose = function () {
    ws = null;
    console.log('onConnectionClose');
    onConnectionClose?.();
    setTimeout(() => {
      connect();
    }, 500);
  };

  ws.onmessage = function (event) {
    /** @type {Message} */
    const message = JSON.parse(event.data);
    console.log('on' + message.type, message);
    switch (message.type) {
      case 'join':
        onJoin(message);
        break;
      case 'leave':
        onLeave(message);
        break;
      case 'message':
        onReceiveMessage(message);
        break;
      case 'ban':
        onBan(message);
        break;
      default:
        console.warn('Receive unknown message', message);
    }
  };
}
