const WebSocket = require('ws');

const wss = new WebSocket.Server({ host: 'localhost', port: 8765 });

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });
  ws.send('something');
});
