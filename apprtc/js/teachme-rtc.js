var whiteboardOn = $('#whiteboard-on');
whiteboardOn.addEventListener('click', toggleWhiteboard);
var miniLocalVideo = $('#miniLocalVideo');
var miniRemoteVideo = $('#miniRemoteVideo');
var whiteboard = $('#whiteboard');
var screenSharing = false;
var videoChat = false;
var remoteScreenSharing = false; 
var tablero = false;
function gotReceiveChannel(event){
  trace('Receive Channel Callback');
  receiveChannel = event.channel;
  receiveChannel.onmessage = handleMessage;
  receiveChannel.onopen = handleReceiveChannelStateChange;
  receiveChannel.onclose = handleReceiveChannelStateChange;
}

function handleReceiveChannelStateChange() {
  var readyState = receiveChannel.readyState;
  console.log('Receive channel state is: ' + readyState);
}

function handleSendChannelStateChange(){
  var readyState = sendChannel.readyState;
  trace('Send channel state is: ' + readyState);
  if (readyState == 'open'){
    console.log('el canal esta abierto');
  } else{
    console.log('el no esta abierto');
  }
}

function sendData(d){
  var data = d;
  if(this.appController.call_.params_.isInitiator) sendChannel.send(data);
  else receiveChannel.send(data);
}

function handleMessage(event){
  trace('receive message: ' + event.data);
  var rec = JSON.parse(event.data);
  console.log('The received message is: ' + event.data);

  switch (rec.fn){
    case 'onTablero':
      if (rec.onTablero){
      onTablero(rec.onTablero);
      console.log('El remoto inicio el tablero.');
      };
      break;
    case 'offTablero':
      if (rec.offTablero) {
        offTablero(rec.offTablero);
        console.log('El remoto detuvo el tablero')
      };
      break;
    case 'engage':
      if (rec.engage) engageRemote(rec.e);
      break;
    case 'disengage':
      if (rec.disengage) disengageRemote('', rec.disengage);
      break;
    case 'putPoint':
      if (rec.putPoint) putPointRemote(rec.e);
      break;
    case 'onScreenSharing':
      remoteScreenSharing = true;
      miniVideo.muted = false;
      break;
    case 'offScreenSharing':
      remoteScreenSharing = false;
      offRemoteScreenSharing();
      break;
    case 'clearBoard':
      clearRemote();
      break;
    case 'undo':
      cUndo();
      break;
    case 'redo':
      cRedo();
      break;
  }
}

function toggleWhiteboard(){
  if (!tablero){
    onTablero(false);
  }else {
    offTablero(false);
  }
}

function onTablero(s){
  tablero = true
  appController.hide_(appController.videosDiv_);
  reattachMediaStream(miniRemoteVideo, remoteVideo);
  reattachMediaStream(miniLocalVideo, appController.miniVideo_);
  appController.deactivate_(remoteVideo);
  appController.deactivate_(appController.miniVideo_);
  remoteVideo.src = '';
  appController.miniVideo_.src = '';
  appController.show_(whiteboard);
  appController.activate_(miniLocalVideo);
  appController.activate_(miniRemoteVideo);
  
  drawConfi();
  // displayButtons(videoChat);
  // if (chat==true){
  //   hideChat();
  //   showChat();
  // }
  if (!s){
    var sender = '{"fn":"onTablero", "onTablero":true}';
    sendData(sender);
  }
}

function offTablero(s){
  if (tablero){
    tablero = false;
    appController.hide_(whiteboard);
    reattachMediaStream(remoteVideo, miniRemoteVideo);
    reattachMediaStream(appController.miniVideo_, miniLocalVideo);
    appController.deactivate_(miniLocalVideo);
    appController.deactivate_(miniRemoteVideo);
    miniRemoteVideo.src = '';
    miniLocalVideo.src = '';
    appController.show_(appController.videosDiv_);
    appController.activate_(remoteVideo);
    appController.activate_(appController.miniVideo_);
    // displayButtons(videoChat);
    // if (chat==true){
    //   hideChat();
    //   showChat();
    // }
    if (!s){
      var sender = '{"fn": "offTablero", "offTablero":true}';
      sendData(sender);
    }
  }
}
