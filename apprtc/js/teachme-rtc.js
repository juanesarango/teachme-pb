var whiteboardOn = $('#whiteboard-on');
whiteboardOn.addEventListener('click', onTablero);

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

function onTablero(s){
  tablero = true
  miniLocalVideo = document.getElementById('miniLocalVideo');
  miniRemoteVideo = document.getElementById('miniRemoteVideo');
  whiteboard = document.getElementById('whiteboard');
  appController.videosDiv_.style.display = "none";
  reattachMediaStream(miniRemoteVideo, remoteVideo);
  reattachMediaStream(miniLocalVideo, appController.miniVideo_);
  //attachMediaStream(miniLocalVideo, localStream);
  remoteVideo.src = '';
  appController.miniVideo_.src = '';
  whiteboard.style.display = "block";
  miniLocalVideo.style.opacity = '1';
  miniRemoteVideo.style.opacity = '1';
  //remoteVideo.style.opacity = '0'
  //miniVideoRemote.style.opacity = '1';
  // drawConfi();
  // displayButtons(videoChat);
  // if (chat==true){
  //   hideChat();
  //   showChat();
  // }
  // if (!s){
  //   var sender = '{"fn":"onTablero", "onTablero":true}';
  //   sendData(sender);
  // }
}

function offTablero(s){
  tablero = false;
  miniLocalVideo = document.getElementById('miniLocalVideo');
  miniRemoteVideo = document.getElementById('miniRemoteVideo');
  whiteboard = document.getElementById('whiteboard');
  whiteboard.style.display = "none";
  reattachMediaStream(remoteVideo, miniRemoteVideo);
  reattachMediaStream(miniVideo, miniLocalVideo);
  miniRemoteVideo.src = '';
  miniLocalVideo.src = '';
  containerDiv.style.display = "block";
  window.onresize();
  displayButtons(videoChat);
  if (chat==true){
    hideChat();
    showChat();
  }
  if (!s){
    var sender = '{"fn": "offTablero", "offTablero":true}';
    sendData(sender);
  }
}
