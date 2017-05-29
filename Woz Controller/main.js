const {app, BrowserWindow, ipcMain} = require('electron')
const path = require('path')
const url = require('url')
var amqp = require('amqplib/callback_api');



// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win


ipcMain.on('asynchronous-command', (event, arg) => {
  amqp.connect('amqp://localhost', function(err, conn) {
    conn.createChannel(function(err, ch) {
      var q = 'command';
      var msg = arg;

      ch.assertQueue(q, {durable: true});
    // Note: on Node 6 Buffer.from(msg) should be used
    ch.sendToQueue(q, new Buffer(msg));
    console.log(" [x] Sent %s", msg);
  });
    setTimeout(function() { conn.close(); }, 500);
  });  
  // event.sender.send('asynchronous-reply', 'pong')
});

ipcMain.on('asynchronous-move', (event, arg) => {
  amqp.connect('amqp://localhost', function(err, conn) {
    conn.createChannel(function(err, ch) {
      var q = 'move_coordinates';
      var msg = arg;

      ch.assertQueue(q, {durable: true});
      // Note: on Node 6 Buffer.from(msg) should be used
      ch.sendToQueue(q, new Buffer(msg));
      console.log(" [x] Sent %s", msg);
  });
    setTimeout(function() { conn.close(); }, 500);
  });  
  // event.sender.send('asynchronous-reply', 'pong')
});



function createWindow () {
  // Create the browser window.
  win = new BrowserWindow({width: 600, height: 800})

  // and load the index.html of the app.
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'app/index.html'),
    protocol: 'file:',
    slashes: true
  }))


  // Open the DevTools.
  // win.webContents.openDevTools()

  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.A