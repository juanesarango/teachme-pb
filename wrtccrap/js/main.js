var localVideo;
var miniVideo;
var remoteVideo;
var localStream;
var remoteStream;
var channel;
var pc;
var socket;
var xmlhttp;
var started = false;
var turnDone = false;
var channelReady = false;
var signalingReady = false;
var tablero = false;
var msgQueue = [];
var chat = false;
var screenSharing = false;
var videoChat = false;
// Set up audio and video regardless of what devices are present.
var sdpConstraints = {'mandatory': {
                      'OfferToReceiveAudio': true,
                      'OfferToReceiveVideo': true }};
var isVideoMuted = false;
var isAudioMuted = false;
// Types of gathered ICE Candidates.
var gatheredIceCandidateTypes = { Local: {}, Remote: {} };

function initialize() {
  if (errorMessages.length > 0) {
    for (i = 0; i < errorMessages.length; ++i) {
      window.alert(errorMessages[i]);
    }
    return;
  }

  console.log('Initializing; room=' + roomKey + '.');
  card = document.getElementById('card');
  localVideo = document.getElementById('localVideo');
  // Reset localVideo display to center.
  localVideo.addEventListener('loadedmetadata', function(){
    window.onresize();});
  miniVideo = document.getElementById('miniVideo');
  remoteVideo = document.getElementById('remoteVideo');
  resetStatus();
  // NOTE: AppRTCClient.java searches & parses this line; update there when
  // changing here.
  openChannel();
  maybeRequestTurn();
  doGetUserMedia();
  // Caller is always ready to create peerConnection.
  signalingReady = initiator;
}

function openChannel() {
  console.log('Opening channel.');
  var channel = new goog.appengine.Channel(channelToken);
  var handler = {
    'onopen': onChannelOpened,
    'onmessage': onChannelMessage,
    'onerror': onChannelError,
    'onclose': onChannelClosed
  };
  socket = channel.open(handler);
}

function maybeRequestTurn() {
  // Skipping TURN Http request for Firefox version <=22.
  // Firefox does not support TURN for version <=22.
  if (webrtcDetectedBrowser === 'firefox' && webrtcDetectedVersion <=22) {
    turnDone = true;
    return;
  }

  for (var i = 0, len = pcConfig.iceServers.length; i < len; i++) {
    if (pcConfig.iceServers[i].url.substr(0, 5) === 'turn:') {
      turnDone = true;
      return;
    }
  }

  var currentDomain = document.domain;
  if (currentDomain.search('localhost') === -1 &&
      currentDomain.search('teachme') === -1) {
    // Not authorized domain. Try with default STUN instead.
    turnDone = true;
    return;
  }

  // No TURN server. Get one from computeengineondemand.appspot.com.
  xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = onTurnResult;
  xmlhttp.open('GET', turnUrl, true);
  xmlhttp.send();
}

function onTurnResult() {
  if (xmlhttp.readyState !== 4)
    return;

  if (xmlhttp.status === 200) {
    var turnServer = JSON.parse(xmlhttp.responseText);
    for (i = 0; i < turnServer.uris.length; i++) {
      // Create a turnUri using the polyfill (adapter.js).
      var iceServer = createIceServer(turnServer.uris[i],
                                      turnServer.username,
                                      turnServer.password);
      if (iceServer !== null) {
        pcConfig.iceServers.push(iceServer);
      }
    }
  } else {
    console.log('Request for TURN server failed.');
  }
  // If TURN request failed, continue the call with default STUN.
  turnDone = true;
  maybeStart();
}

function resetStatus() {
  if (!initiator) {
    setStatus('Esperando a que la otra persona se una a la sesión de Teachme ');
  } else {
    setStatus('Inicializando la sesión de Teachme...');
  }
}

function doGetUserMedia() {
  // Call into getUserMedia via the polyfill (adapter.js).
  try {
    getUserMedia(mediaConstraints, onUserMediaSuccess,
                 onUserMediaError);
    console.log('Requested access to local media with mediaConstraints:\n' +
                '  \'' + JSON.stringify(mediaConstraints) + '\'');
  } catch (e) {
    alert('Hubo un error al intentar acceder a la WebCam. Es este un explorador que soporta WebRTC?');
    console.log('getUserMedia failed with exception: ' + e.message);
  }
}

function createPeerConnection() {
  try {
    // Create an RTCPeerConnection via the polyfill (adapter.js).
    pc = new RTCPeerConnection(pcConfig, pcConstraints);
    pc.onicecandidate = onIceCandidate;
    console.log('Created RTCPeerConnnection with:\n' +
                '  config: \'' + JSON.stringify(pcConfig) + '\';\n' +
                '  constraints: \'' + JSON.stringify(pcConstraints) + '\'.');
  } catch (e) {
    console.log('Failed to create PeerConnection, exception: ' + e.message);
    alert('No se pudo crear un objeto RTCPeerConnection; \
          Este explorador no soporta el protocolo WebRTC.');
      return;
  }
  pc.onaddstream = onRemoteStreamAdded;
  pc.onremovestream = onRemoteStreamRemoved;
  pc.onsignalingstatechange = onSignalingStateChanged;
  pc.oniceconnectionstatechange = onIceConnectionStateChanged;

  if(initiator){
    try{
      //crear el canal de datos
      sendChannel = pc.createDataChannel("sendDataChannel", {reliable: true});
      trace('Created send data channel');
    }catch(e){
      alert('Error al intentar crear el canal');
      trace('createDataChannel failed with exception: ' + e.message);
    }
    sendChannel.onopen = handleSendChannelStateChange;
    sendChannel.onmessage = handleMessage;
    sendChannel.onclose = handleSendChannelStateChange;
  } else { //joiner
    pc.ondatachannel = gotReceiveChannel;
  }
}

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
  if (readyState == "open"){
    console.log("el canal esta abierto")
  } else{
    console.log("el no esta abierto")
  }
}

function sendData(d){
  var data = d;
  if(initiator) sendChannel.send(data);
  else receiveChannel.send(data);
  trace('send data: ' + data);
}
var rec;

function handleMessage(event){
  //trace('receive message: ' + event.data);
  rec = JSON.parse(event.data);
  console.log("el mensaje recibido: " + event.data);

  switch (rec.fn){
    case "onTablero":
      if (rec.onTablero){
      onTablero(rec.onTablero);
      console.log("El remoto inicio el tablero.");
      };
      break;
    case "offTablero":
      if (rec.offTablero) {
        offTablero(rec.offTablero);
        console.log("El remoto detuvo el tablero")
      };
      break;
    case "engage":
      if (rec.engage) engageRemote(rec.e);
      break;
    case "disengage":
      if (rec.disengage) disengageRemote("", rec.disengage);
      break;
    case "putPoint":
      if (rec.putPoint) putPointRemote(rec.e);
      break;
  }
}

function maybeStart() {
  if (!started && signalingReady &&
      localStream && channelReady && turnDone) {
    displayButtons(false);
    console.log('Creating PeerConnection.');
    createPeerConnection();
    console.log('Adding local stream.');
    pc.addStream(localStream);
    started = true;

    if (initiator)
      doCall();
    else
      calleeStart();
  }
}

function setStatus(state) {
  document.getElementById('status').innerHTML = state;
}

function doCall() {
  var constraints = mergeConstraints(offerConstraints, sdpConstraints);
  console.log('Sending offer to peer, with constraints: \n' +
              '  \'' + JSON.stringify(constraints) + '\'.')
  pc.createOffer(setLocalAndSendMessage,
                 onCreateSessionDescriptionError, constraints);
}

function calleeStart() {
  // Callee starts to process cached offer and other messages.
  while (msgQueue.length > 0) {
    processSignalingMessage(msgQueue.shift());
  }
}

function doAnswer() {
  console.log('Sending answer to peer.');
  pc.createAnswer(setLocalAndSendMessage,
                  onCreateSessionDescriptionError, sdpConstraints);
}

function mergeConstraints(cons1, cons2) {
  var merged = cons1;
  for (var name in cons2.mandatory) {
    merged.mandatory[name] = cons2.mandatory[name];
  }
  merged.optional.concat(cons2.optional);
  return merged;
}

function setLocalAndSendMessage(sessionDescription) {
  sessionDescription.sdp = maybePreferAudioReceiveCodec(sessionDescription.sdp);
  pc.setLocalDescription(sessionDescription,
       onSetSessionDescriptionSuccess, onSetSessionDescriptionError);
  sendMessage(sessionDescription);
}

function setRemote(message) {
  // Set Opus in Stereo, if stereo enabled.
  if (stereo)
    message.sdp = addStereo(message.sdp);
  message.sdp = maybePreferAudioSendCodec(message.sdp);
  pc.setRemoteDescription(new RTCSessionDescription(message),
       onSetSessionDescriptionSuccess, onSetSessionDescriptionError);
}

function sendMessage(message) {
  var msgString = JSON.stringify(message);
  console.log('C->S: ' + msgString);
  // NOTE: AppRTCClient.java searches & parses this line; update there when
  // changing here.
  path = '/session/message?r=' + roomKey + '&u=' + me;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send(msgString);
}

function processSignalingMessage(message) {
  if (!started) {
    console.log('peerConnection has not been created yet!');
    return;
  }

  if (message.type === 'offer') {
    setRemote(message);
    doAnswer();
  } else if (message.type === 'answer') {
    setRemote(message);
  } else if (message.type === 'candidate') {
    var candidate = new RTCIceCandidate({sdpMLineIndex: message.label,
                                         candidate: message.candidate});
    noteIceCandidate("Remote", iceCandidateType(message.candidate));
    pc.addIceCandidate(candidate);
  } else if (message.type === 'bye') {
    onRemoteHangup();
  }
}

function onChannelOpened() {
  console.log('Channel opened.');
  channelReady = true;
  maybeStart();
}
function onChannelMessage(message) {
  console.log('S->C: ' + message.data);
  var msg = JSON.parse(message.data);
  // Since the turn response is async and also GAE might disorder the
  // Message delivery due to possible datastore query at server side,
  // So callee needs to cache messages before peerConnection is created.
  if (msg.type === 'chat') { 
    var p = document.createElement("h6");
    if (msg.userid == usuarioChat) {
      p.innerHTML = '<span class="logsend"><strong>' + msg.userid + '</strong>' + ': ' + msg.message + '</span>';
      document.getElementById("chat").value = "";   
    } else {
      p.innerHTML = '<span class="logreceive"><strong>' + msg.userid + '</strong>' + ': ' + msg.message + '</span>';
    }
    document.getElementById("logchat").appendChild(p);
  }
  if (!initiator && !started) {
    if (msg.type === 'offer') {
      // Add offer to the beginning of msgQueue, since we can't handle
      // Early candidates before offer at present.
      msgQueue.unshift(msg);
      // Callee creates PeerConnection
      signalingReady = true;
      maybeStart();
    } else {
      msgQueue.push(msg);
    }
  } else {
    processSignalingMessage(msg);
  }
}
function onChannelError() {
  console.log('Channel error.');
}
function onChannelClosed() {
  console.log('Channel closed.');
}

function onUserMediaSuccess(stream) {
  console.log('User has granted access to local media.');
  // Call the polyfill wrapper to attach the media stream to this element.
  attachMediaStream(localVideo, stream);
  localVideo.style.opacity = 1;
  localStream = stream;
  // Caller creates PeerConnection.
  maybeStart();
}

function onUserMediaError(error) {
  console.log('Failed to get access to local media. Error code was ' +
              error.code);
  alert('No se pudo acceder a local media. El codigo del error  es ' +
        error.code + '.');
}

function onCreateSessionDescriptionError(error) {
  console.log('Failed to create session description: ' + error.toString());
}

function onSetSessionDescriptionSuccess() {
  console.log('Set session description success.');
}

function onSetSessionDescriptionError(error) {
  console.log('Failed to set session description: ' + error.toString());
}

function iceCandidateType(candidateSDP) {
  if (candidateSDP.indexOf("typ relay ") >= 0)
    return "TURN";
  if (candidateSDP.indexOf("typ srflx ") >= 0)
    return "STUN";
  if (candidateSDP.indexOf("typ host ") >= 0)
    return "HOST";
  return "UNKNOWN";
}

function onIceCandidate(event) {
  if (event.candidate) {
    sendMessage({type: 'candidate',
                 label: event.candidate.sdpMLineIndex,
                 id: event.candidate.sdpMid,
                 candidate: event.candidate.candidate});
    noteIceCandidate("Local", iceCandidateType(event.candidate.candidate));
  } else {
    console.log('End of candidates.');
  }
}

function onRemoteStreamAdded(event) {
  console.log('Remote stream added.');
  reattachMediaStream(miniVideo, localVideo);
  attachMediaStream(remoteVideo, event.stream);
  remoteStream = event.stream;
  waitForRemoteVideo();
}

function onRemoteStreamRemoved(event) {
  console.log('Remote stream removed.');
}

function onSignalingStateChanged(event) {
  updateInfoDiv();
}

function onIceConnectionStateChanged(event) {
  updateInfoDiv();
}

function onHangup() {
  console.log('Hanging up.');
  transitionToDone();
  localStream.stop();
  stop();
  // will trigger BYE from server
  socket.close();
}

function onRemoteHangup() {
  console.log('Session terminated.');
  initiator = 0;
  transitionToWaiting();
  stop();
}

function stop() {
  started = false;
  signalingReady = false;
  isAudioMuted = false;
  isVideoMuted = false;
  pc.close();
  pc = null;
  msgQueue.length = 0;
}

function waitForRemoteVideo() {
  // Call the getVideoTracks method via adapter.js.
  videoTracks = remoteStream.getVideoTracks();
  if (videoTracks.length === 0 || remoteVideo.currentTime > 0) {
    transitionToActive();
  } else {
    setTimeout(waitForRemoteVideo, 100);
  }
}

function transitionToActive() {
  remoteVideo.style.opacity = 1;
  card.style.webkitTransform = 'rotateY(180deg)';
  setTimeout(function() { localVideo.src = ''; }, 500);
  setTimeout(function() { miniVideo.style.opacity = 1; }, 1000);
  // Reset window display according to the asperio of remote video.
  window.onresize();
  videoChat = true;
  displayButtons(videoChat);
}

function transitionToWaiting() {
  card.style.webkitTransform = 'rotateY(0deg)';
  setTimeout(function() {
               localVideo.src = miniVideo.src;
               miniVideo.src = '';
               remoteVideo.src = '' }, 500);
  miniVideo.style.opacity = 0;
  remoteVideo.style.opacity = 0;
  resetStatus();
}

function transitionToDone() {
  localVideo.style.opacity = 0;
  remoteVideo.style.opacity = 0;
  miniVideo.style.opacity = 0;
  setStatus('Has abandonado la sesión de Teachme. <a href=' + roomLink + '>\
            Haz click aquí</a> para unirte de nuevo.');
}

function enterFullScreen() {
  container.webkitRequestFullScreen();
}

function noteIceCandidate(location, type) {
  if (gatheredIceCandidateTypes[location][type])
    return;
  gatheredIceCandidateTypes[location][type] = 1;
  updateInfoDiv();
}

function getInfoDiv() {
  return document.getElementById("infoDiv");
}

function updateInfoDiv() {
  var contents = "<pre>Gathered ICE Candidates\n";
  for (var endpoint in gatheredIceCandidateTypes) {
    contents += endpoint + ":\n";
    for (var type in gatheredIceCandidateTypes[endpoint])
      contents += "  " + type + "\n";
  }
  if (pc != null) {
    contents += "Gathering: " + pc.iceGatheringState + "\n";
    contents += "</pre>\n";
    contents += "<pre>PC State:\n";
    contents += "Signaling: " + pc.signalingState + "\n";
    contents += "ICE: " + pc.iceConnectionState + "\n";
  }
  var div = getInfoDiv();
  div.innerHTML = contents + "</pre>";
}

function toggleInfoDivDisplay() {
  var div = getInfoDiv();
  if (div.style.display == "block") {
    div.style.display = "none";
  } else {
    div.style.display = "block";
  }
}

function toggleVideoMute() {
  // Call the getVideoTracks method via adapter.js.
  videoTracks = localStream.getVideoTracks();

  if (videoTracks.length === 0) {
    console.log('No local video available.');
    return;
  }

  if (isVideoMuted) {
    for (i = 0; i < videoTracks.length; i++) {
      videoTracks[i].enabled = true;
    }
    console.log('Video unmuted.');
  } else {
    for (i = 0; i < videoTracks.length; i++) {
      videoTracks[i].enabled = false;
    }
    console.log('Video muted.');
  }

  isVideoMuted = !isVideoMuted;
}

function toggleAudioMute() {
  // Call the getAudioTracks method via adapter.js.
  audioTracks = localStream.getAudioTracks();

  if (audioTracks.length === 0) {
    console.log('No local audio available.');
    return;
  }

  if (isAudioMuted) {
    for (i = 0; i < audioTracks.length; i++) {
      audioTracks[i].enabled = true;
    }
    console.log('Audio unmuted.');
  } else {
    for (i = 0; i < audioTracks.length; i++){
      audioTracks[i].enabled = false;
    }
    console.log('Audio muted.');
  }

  isAudioMuted = !isAudioMuted;
}

// Mac: hotkey is Command.
// Non-Mac: hotkey is Control.
// <hotkey>-D: toggle audio mute.
// <hotkey>-E: toggle video mute.
// <hotkey>-I: toggle Info box.
// Return false to screen out original Chrome shortcuts.
document.onkeydown = function(event) {
  var hotkey = event.ctrlKey;
  if (navigator.appVersion.indexOf('Mac') != -1)
    hotkey = event.metaKey;
  if (!hotkey)
    return;
  switch (event.keyCode) {
    case 68:
      toggleAudioMute();
      return false;
    case 69:
      toggleVideoMute();
      return false;
    case 73:
      toggleInfoDivDisplay();
      return false;
    default:
      return;
  }
}

function maybePreferAudioSendCodec(sdp) {
  if (audio_send_codec == '') {
    console.log('No preference on audio send codec.');
    return sdp;
  }
  console.log('Prefer audio send codec: ' + audio_send_codec);
  return preferAudioCodec(sdp, audio_send_codec);
}

function maybePreferAudioReceiveCodec(sdp) {
  if (audio_receive_codec == '') {
    console.log('No preference on audio receive codec.');
    return sdp;
  }
  console.log('Prefer audio receive codec: ' + audio_receive_codec);
  return preferAudioCodec(sdp, audio_receive_codec);
}

// Set |codec| as the default audio codec if it's present.
// The format of |codec| is 'NAME/RATE', e.g. 'opus/48000'.
function preferAudioCodec(sdp, codec) {
  var fields = codec.split('/');
  if (fields.length != 2) {
    console.log('Invalid codec setting: ' + codec);
    return sdp;
  }
  var name = fields[0];
  var rate = fields[1];
  var sdpLines = sdp.split('\r\n');

  // Search for m line.
  for (var i = 0; i < sdpLines.length; i++) {
      if (sdpLines[i].search('m=audio') !== -1) {
        var mLineIndex = i;
        break;
      }
  }
  if (mLineIndex === null)
    return sdp;

  // If the codec is available, set it as the default in m line.
  for (var i = 0; i < sdpLines.length; i++) {
    if (sdpLines[i].search(name + '/' + rate) !== -1) {
      var regexp = new RegExp(':(\\d+) ' + name + '\\/' + rate, 'i');
      var payload = extractSdp(sdpLines[i], regexp);
      if (payload)
        sdpLines[mLineIndex] = setDefaultCodec(sdpLines[mLineIndex],
                                               payload);
      break;
    }
  }

  // Remove CN in m line and sdp.
  sdpLines = removeCN(sdpLines, mLineIndex);

  sdp = sdpLines.join('\r\n');
  return sdp;
}

// Set Opus in stereo if stereo is enabled.
function addStereo(sdp) {
  var sdpLines = sdp.split('\r\n');

  // Find opus payload.
  for (var i = 0; i < sdpLines.length; i++) {
    if (sdpLines[i].search('opus/48000') !== -1) {
      var opusPayload = extractSdp(sdpLines[i], /:(\d+) opus\/48000/i);
      break;
    }
  }

  // Find the payload in fmtp line.
  for (var i = 0; i < sdpLines.length; i++) {
    if (sdpLines[i].search('a=fmtp') !== -1) {
      var payload = extractSdp(sdpLines[i], /a=fmtp:(\d+)/ );
      if (payload === opusPayload) {
        var fmtpLineIndex = i;
        break;
      }
    }
  }
  // No fmtp line found.
  if (fmtpLineIndex === null)
    return sdp;

  // Append stereo=1 to fmtp line.
  sdpLines[fmtpLineIndex] = sdpLines[fmtpLineIndex].concat(' stereo=1');

  sdp = sdpLines.join('\r\n');
  return sdp;
}

function extractSdp(sdpLine, pattern) {
  var result = sdpLine.match(pattern);
  return (result && result.length == 2)? result[1]: null;
}

// Set the selected codec to the first in m line.
function setDefaultCodec(mLine, payload) {
  var elements = mLine.split(' ');
  var newLine = new Array();
  var index = 0;
  for (var i = 0; i < elements.length; i++) {
    if (index === 3) // Format of media starts from the fourth.
      newLine[index++] = payload; // Put target payload to the first.
    if (elements[i] !== payload)
      newLine[index++] = elements[i];
  }
  return newLine.join(' ');
}

// Strip CN from sdp before CN constraints is ready.
function removeCN(sdpLines, mLineIndex) {
  var mLineElements = sdpLines[mLineIndex].split(' ');
  // Scan from end for the convenience of removing an item.
  for (var i = sdpLines.length-1; i >= 0; i--) {
    var payload = extractSdp(sdpLines[i], /a=rtpmap:(\d+) CN\/\d+/i);
    if (payload) {
      var cnPos = mLineElements.indexOf(payload);
      if (cnPos !== -1) {
        // Remove CN payload from m line.
        mLineElements.splice(cnPos, 1);
      }
      // Remove CN line in sdp
      sdpLines.splice(i, 1);
    }
  }

  sdpLines[mLineIndex] = mLineElements.join(' ');
  return sdpLines;
}

// Send BYE on refreshing(or leaving) a demo page
// to ensure the room is cleaned for next session.
window.onbeforeunload = function() {
  sendMessage({type: 'bye'});
}

//Juanes
function onChat(){
  message_user = document.getElementById("chat").value;
  sendMessage({type: 'chat', message: message_user, userid: usuarioChat});  
}

// Set the video diplaying in the center of window.
window.onresize = function(){
  if (!tablero){
      var aspectRatio;
      if (remoteVideo.style.opacity === '1') {
        aspectRatio = remoteVideo.videoWidth/remoteVideo.videoHeight;
      } else if (localVideo.style.opacity === '1') {
        aspectRatio = localVideo.videoWidth/localVideo.videoHeight;
      } else {
        return;
      }

      var innerHeight = this.innerHeight;
      var innerWidth = this.innerWidth;
      var videoWidth = innerWidth < aspectRatio * window.innerHeight ?
                       innerWidth : aspectRatio * window.innerHeight;
      var videoHeight = innerHeight < window.innerWidth / aspectRatio ?
                        innerHeight : window.innerWidth / aspectRatio;
      containerDiv = document.getElementById('container');
      containerDiv.style.width = videoWidth + 'px';
      containerDiv.style.height = videoHeight + 'px';
      containerDiv.style.left = (innerWidth - videoWidth) / 2 + 'px';
      containerDiv.style.top = (innerHeight - videoHeight) / 2 + 'px';
  }
};

function showChat(){
  chatbox = document.getElementById('chatbox');
  chatbox.style.display = "block";
  if (tablero == false){
    chatbox.style.left = "20%";
    chatbox.style.marginLeft= "0%"; 
  } else {
    chatbox.style.left = "-161px";
    chatbox.style.marginLeft= "50%";
  }

  chat = true;
  displayButtons(videoChat);
}

function hideChat(){
  chatbox = document.getElementById('chatbox');
  chatbox.style.display = "none";
  chat = false;
  displayButtons(videoChat);
}

function displayButtons(vd){
  if (chat == false){
    btnChat = '<input type=\'button\' id=\'chatbtn\' class=\'btn btn-info\' value=\'Mostrar chat\' onclick=\'showChat()\' />'; 
  } else {
    btnChat = '<input type=\'button\' id=\'chatbtn\' class=\'btn btn-warning\' value=\'Esconder chat\' onclick=\'hideChat()\' />';
  }
  if (tablero == false){
    btnTablero = '<input type=\'button\' id=\'tablero\' class=\'btn btn-info\' value=\'Iniciar tablero\' onclick=\'onTablero()\' />';
  } else {
    btnTablero = '<input type=\'button\' id=\'tablero\' class=\'btn btn-warning\' value=\'Detener tablero\' onclick=\'offTablero()\' />';
  }
  if (screenSharing == false){
    btnScreenSharing = '<input type=\'button\' id=\'screenSharing\' class=\'btn btn-info\' value=\'Compartir Pantalla\' onclick=\'onScreenSharing()\' />';
  } else {
    btnScreenSharing = '<input type=\'button\' id=\'screenSharing\' class=\'btn btn-warning\' value=\'Detener Compartir Pantalla\' onclick=\'offScreenSharing()\' />';
  }
  if (vd== true){
    btnVD = '<input type=\'button\' id=\'hangup\' class=\'btn btn-danger\' value=\'Terminar sesión\' onclick=\'onHangup()\' />';
    videoChat = true;
  } else {
    btnVD = 'Conectando...         ';
    btnTablero = ' ';
    btnScreenSharing = ' ';
    videoChat = false;
  }
  setStatus(btnVD  + btnTablero + btnChat + btnScreenSharing);
}

function onTablero(s){
  tablero = true
  drawLocalVideo = document.getElementById('drawLocalVideo');
  drawRemoteVideo = document.getElementById('drawRemoteVideo');
  drawingApp = document.getElementById('drawingapp');
  containerDiv.style.display = "none";
  reattachMediaStream(drawRemoteVideo, remoteVideo);
  reattachMediaStream(drawLocalVideo, miniVideo);
  //attachMediaStream(drawLocalVideo, localStream);
  remoteVideo.src = '';
  miniVideo.src = '';
  drawingApp.style.display = "block";
  drawLocalVideo.style.opacity = '1';
  drawRemoteVideo.style.opacity = '1';
  //remoteVideo.style.opacity = '0'
  //miniVideoRemote.style.opacity = '1';
  drawingApp.style.height = window.innerHeight*0.9;
  drawConfi();
  displayButtons(videoChat);
  if (chat==true){
    hideChat();
    showChat();
  }
  if (!s){
    var sender = '{"fn":"onTablero", "onTablero":true}';
    sendData(sender);
  }
}

function offTablero(s){
  tablero = false;
  drawLocalVideo = document.getElementById('drawLocalVideo');
  drawRemoteVideo = document.getElementById('drawRemoteVideo');
  drawingApp = document.getElementById('drawingapp');
  drawingApp.style.display = "none";
  reattachMediaStream(remoteVideo, drawRemoteVideo);
  reattachMediaStream(miniVideo, drawLocalVideo);
  drawRemoteVideo.src = '';
  drawLocalVideo.src = '';
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

function onScreenSharing(){
  navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.getUserMedia;
  navigator.getUserMedia({
    video: {
      mandatory: {
        chromeMediaSource: 'screen'
        // maxWidth: 640,
        // maxHeight: 480
      }
    }
  }, function(stream) {
    attachMediaStream(localVideo, stream);
    pc.removeStream(localStream);
    pc.addStream(stream);
   }, function() {
      console.log('Hay error');
   }
  )
}

