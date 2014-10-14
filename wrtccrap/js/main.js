/*
 *  Copyright (c) 2014 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

/* More information about these options at jshint.com/docs/options */
/* jshint browser: true, camelcase: true, curly: true, devel: true, eqeqeq: true, forin: false, globalstrict: true, quotmark: single, undef: true, unused: strict */
/* global attachMediaStream, audioRecvBitrate, audioRecvCodec, audioSendBitrate, audioSendCodec, channelToken, createIceServers, errorMessages, getUserMedia, goog, initiator:true, me, mediaConstraints, offerConstraints, pcConfig, pcConstraints, reattachMediaStream, roomKey, roomLink, RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, setupStereoscopic, stereo, stereoscopic, trace, turnUrl, videoRecvBitrate, videoSendBitrate, videoSendInitialBitrate:true */
/* exported enterFullScreen, initialize, onHangup */

'use strict';

var localVideo;
var miniVideo;
var remoteVideo;
var hasLocalStream;
var localStream;
var remoteStream;
var pc;
var socket;
var xmlhttp;
var started = false;
var turnDone = false;
var channelReady = false;
var signalingReady = false;
var msgQueue = [];
var card;
var containerDiv;

var chat = false;
var screenSharing = false;
var videoChat = false;
var remoteScreenSharing = false; 
var tablero = false;
var channel;
var localScreenStream;
var remoteScreenStream;
var sendChannel;
var receiveChannel;
var drawLocalVideo;
var drawRemoteVideo;
var drawingApp;
var chatbox;

// Set up audio and video regardless of what devices are present.
// Disable comfort noise for maximum audio quality.
var sdpConstraints = {
  'mandatory': {
    'OfferToReceiveAudio': true,
    'OfferToReceiveVideo': true
  },
  'optional': [{
    'VoiceActivityDetection': false
  }]
};
var isVideoMuted = false;
var isAudioMuted = false;

// Stats for info div.
var startTime, endTime;
var gatheredIceCandidateTypes = {
  Local: {},
  Remote: {}
};
var infoDivErrors = [];
var stats;
var getStatsTimer;

function initialize() {
  if (errorMessages.length > 0) {
    for (var i = 0; i < errorMessages.length; ++i) {
      window.alert(errorMessages[i]);
    }
    return;
  }

  trace('Initializing; room=' + roomKey + '.');
  card = document.getElementById('card');
  containerDiv = document.getElementById('container');
  localVideo = document.getElementById('localVideo');
  // Reset localVideo display to center.
  localVideo.addEventListener('loadedmetadata', function() {
    window.onresize();
  });
  miniVideo = document.getElementById('miniVideo');
  remoteVideo = document.getElementById('remoteVideo');
  resetStatus();
  // NOTE: AppRTCClient.java searches & parses this line; update there when
  // changing here.
  openChannel();
  maybeRequestTurn();

  // Caller is always ready to create peerConnection.
  signalingReady = initiator;

  if (mediaConstraints.audio === false &&
      mediaConstraints.video === false) {
    hasLocalStream = false;
    maybeStart();
  } else {
    hasLocalStream = true;
    doGetUserMedia();
  }
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
  // Allow to skip turn by passing ts=false to apprtc.
  if (turnUrl === '') {
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
  if (xmlhttp.readyState !== 4) {
    return;
  }

  if (xmlhttp.status === 200) {
    var turnServer = JSON.parse(xmlhttp.responseText);
    // Create turnUris using the polyfill (adapter.js).
    var iceServers = createIceServers(turnServer.uris,
        turnServer.username, turnServer.password);
    if (iceServers !== null) {
      pcConfig.iceServers = pcConfig.iceServers.concat(iceServers);
    }
  } else {
    messageError('No TURN server; unlikely that media will traverse networks. ' +
        'If this persists please report it to ' +
        'discuss-webrtc@googlegroups.com.');
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
    trace('Created RTCPeerConnnection with:\n' +
        '  config: \'' + JSON.stringify(pcConfig) + '\';\n' +
        '  constraints: \'' + JSON.stringify(pcConstraints) + '\'.');
  } catch (e) {
    messageError('Failed to create PeerConnection, exception: ' + e.message);
    alert('Cannot create RTCPeerConnection object; ' +
        'WebRTC is not supported by this browser.');
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
    case "onScreenSharing":
      remoteScreenSharing = true;
      miniVideo.muted = false;
      break;
    case "offScreenSharing":
      remoteScreenSharing = false;
      offRemoteScreenSharing();
      break;
    case "clearBoard":
      clearRemote();
      break;
    case "undo":
      cUndo();
      break;
    case "redo":
      cRedo();
      break;
  }
}

function maybeStart() {
  if (!started && signalingReady && channelReady && turnDone &&
      (localStream || !hasLocalStream)) {
    startTime = window.performance.now();
    setStatus('Connecting...');
    trace('Creating PeerConnection.');
    createPeerConnection();

    if (hasLocalStream) {
      trace('Adding local stream.');
      pc.addStream(localStream);
    } else {
      trace('Not sending any stream.');
    }
    started = true;

    if (initiator) {
      doCall();
    } else {
      calleeStart();
    }
  }
}

function setStatus(state) {
  document.getElementById('status').innerHTML = state;
}

function doCall() {
  var constraints = mergeConstraints(offerConstraints, sdpConstraints);
  trace('Sending offer to peer, with constraints: \n' +
      '  \'' + JSON.stringify(constraints) + '\'.');
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
  trace('Sending answer to peer.');
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
  sessionDescription.sdp = maybeSetAudioReceiveBitRate(sessionDescription.sdp);
  sessionDescription.sdp = maybeSetVideoReceiveBitRate(sessionDescription.sdp);
  pc.setLocalDescription(sessionDescription,
      onSetSessionDescriptionSuccess, onSetSessionDescriptionError);
  sendMessage(sessionDescription);
}

function setRemote(message) {
  // Set Opus in Stereo, if stereo enabled.
  if (stereo) {
    message.sdp = addCodecParam(message.sdp, 'opus/48000', 'stereo=1');
  }
  if (opusfec) {
    message.sdp = addCodecParam(message.sdp, 'opus/48000', 'useinbandfec=1');
  }
  // Set Opus maxplaybackrate, if requested.
  if (opusMaxPbr) {
    message.sdp = addCodecParam(message.sdp, 'opus/48000', 'maxplaybackrate=' +
        opusMaxPbr);
  }
  message.sdp = maybePreferAudioSendCodec(message.sdp);
  message.sdp = maybeSetAudioSendBitRate(message.sdp);
  message.sdp = maybeSetVideoSendBitRate(message.sdp);
  message.sdp = maybeSetVideoSendInitialBitRate(message.sdp);
  pc.setRemoteDescription(new RTCSessionDescription(message),
      onSetRemoteDescriptionSuccess, onSetSessionDescriptionError);

  function onSetRemoteDescriptionSuccess() {
    trace('Set remote session description success.');
    // By now all onaddstream events for the setRemoteDescription have fired,
    // so we can know if the peer has any remote video streams that we need
    // to wait for. Otherwise, transition immediately to the active state.
    // NOTE: Ideally we could just check |remoteStream| here, which is populated
    // in the onaddstream callback. But as indicated in
    // https://code.google.com/p/webrtc/issues/detail?id=3358, sometimes this
    // callback is dispatched after the setRemoteDescription success callback.
    // Therefore, we read the remoteStreams array directly from the
    // PeerConnection, which seems to work reliably.
    var remoteStreams = pc.getRemoteStreams();
    if (remoteStreams.length > 0 &&
        remoteStreams[0].getVideoTracks().length > 0) {
      trace('Waiting for remote video.');
      waitForRemoteVideo();
    } else {
      // TODO(juberti): Make this wait for ICE connection before transitioning.
      trace('No remote video stream; not waiting for media to arrive.');
      transitionToActive();
    }
  }
}

function sendMessage(message) {
  var msgString = JSON.stringify(message);
  console.log('C->S: ' + msgString);
  // NOTE: AppRTCClient.java searches & parses this line; update there when
  // changing here.
  var path = '/session/message?r=' + roomKey + '&u=' + me;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send(msgString);
}

function processSignalingMessage(message) {
  if (!started) {
    messageError('peerConnection has not been created yet!');
    return;
  }

  if (message.type === 'offer') {
    setRemote(message);
    doAnswer();
  } else if (message.type === 'answer') {
    setRemote(message);
  } else if (message.type === 'candidate') {
    var candidate = new RTCIceCandidate({
      sdpMLineIndex: message.label,
      candidate: message.candidate
    });
    noteIceCandidate('Remote', iceCandidateType(message.candidate));
    pc.addIceCandidate(candidate,
        onAddIceCandidateSuccess, onAddIceCandidateError);
  } else if (message.type === 'bye') {
    onRemoteHangup();
  }
}

function onAddIceCandidateSuccess() {
  trace('Remote candidate added successfully.');
}

function onAddIceCandidateError(error) {
  messageError('Failed to add remote candidate: ' + error.toString());
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

function messageError(msg) {
  trace(msg);
  infoDivErrors.push(msg);
  updateInfoDiv();
  showInfoDiv();
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
  var errorMessage = 'Failed to get access to local media. Error name was ' +
      error.name + '. Continuing without sending a stream.';
  messageError(errorMessage);
  alert(errorMessage);

  hasLocalStream = false;
  maybeStart();
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
  switch (candidateSDP.split(' ')[7]) {
    case 'host':
      return 'HOST';
    case 'srflx':
      return 'STUN';
    case 'relay':
      return 'TURN';
    default:
      return 'UNKNOWN';
  }
}

function onIceCandidate(event) {
  if (event.candidate) {
    if (pcConfig.iceTransports === 'relay') {
      // Filter out non relay Candidates, if iceTransports is set to relay.
      if (event.candidate.candidate.search('relay') === -1) {
        return;
      }
    }
    sendMessage({
      type: 'candidate',
      label: event.candidate.sdpMLineIndex,
      id: event.candidate.sdpMid,
      candidate: event.candidate.candidate
    });
    noteIceCandidate('Local', iceCandidateType(event.candidate.candidate));
  } else {
    trace('End of candidates.');
  }
}

function onRemoteStreamAdded(event) {
  console.log('Remote stream added.');
  if (remoteScreenSharing == false){
    reattachMediaStream(miniVideo, localVideo);
    remoteStream = event.stream;
  }else{
    reattachMediaStream(miniVideo, remoteVideo);
    miniVideo.muted = false;
    remoteScreenStream = event.stream;
  }
  attachMediaStream(remoteVideo, event.stream);
  remoteStream = event.stream;
}

function refreshStats() {
  if (pc) {
    pc.getStats(function(response) {
      stats = response.result();
      updateInfoDiv();
    });
  }
}

// Return the integer stat |statName| from the object with type |statObj| in
// |stats|, or null if not present.
function extractStatAsInt(stats, statObj, statName) {
  // Ignore stats that have a 'nullish' value.
  // The correct fix is indicated in
  // https://code.google.com/p/webrtc/issues/detail?id=3377.
  var str = extractStat(stats, statObj, statName);
  if (str) {
    var val = parseInt(str);
    if (val !== -1) {
      return val;
    }
  }
  return null;
}

// Return the stat |statName| from the object with type |statObj| in |stats|
// as a string, or null if not present.
function extractStat(stats, statObj, statName) {
  var report = getStatsReport(stats, statObj, statName);
  if (report && report.names().indexOf(statName) !== -1) {
    return report.stat(statName);
  }
  return null;
}

// Return the stats report with type |statObj| in |stats|, with the stat
// |statName| (if specified), and value |statVal| (if specified). Return
// undef if not present.
function getStatsReport(stats, statObj, statName, statVal) {
  if (stats) {
    for (var i = 0; i < stats.length; ++i) {
      var report = stats[i];
      if (report.type === statObj) {
        var found = true;
        // If |statName| is present, ensure |report| has that stat.
        // If |statVal| is present, ensure the value matches.
        if (statName) {
          var val = report.stat(statName);
          found = statVal !== undefined ? val === statVal : val;
        }
        if (found) {
          return report;
        }
      }
    }
  }
}

function computeE2EDelay(captureStart, remoteVideoCurrentTime) {
  // Computes end to end Delay.
  if (captureStart) {
    // Adding offset to get NTP time.
    var nowNTP = Date.now() + 2208988800000;
    var e2eDelay = nowNTP - captureStart - remoteVideoCurrentTime * 1000;
    return e2eDelay.toFixed(0);
  }
  return null;
}

function onRemoteStreamRemoved() {
  trace('Remote stream removed.');
}

function onSignalingStateChanged() {
  if (pc) {
    trace('Signaling state changed to: ' + pc.signalingState);
  }
  updateInfoDiv();
}

function onIceConnectionStateChanged() {
  if (pc) {
    trace('ICE connection state changed to: ' + pc.iceConnectionState);
  }
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
  remoteStream = null;
  msgQueue.length = 0;
}

function waitForRemoteVideo() {
  // Wait for the actual video to start arriving before moving to the active
  // call state.
  if (remoteVideo.currentTime > 0) {
    transitionToActive();
  } else {
    setTimeout(waitForRemoteVideo, 10);
  }
}

function transitionToActive() {
  endTime = window.performance.now();
  trace('Call setup time: ' + (endTime - startTime).toFixed(0) + 'ms.');
  updateInfoDiv();
  // Prepare the remote video and PIP elements.
  if (stereoscopic) {
    setupStereoscopic(remoteVideo, document.getElementById('remoteCanvas'));
  } else {
    reattachMediaStream(miniVideo, localVideo);
  }
  miniVideo.style.opacity = 1;
  remoteVideo.style.opacity = 1;
  // Spin the card to show remote video (800 ms). Set a timer to detach the
  // local video once the transition completes.
  card.style.webkitTransform = 'rotateY(180deg)';
  setTimeout(function() {
    localVideo.src = '';
  }, 800);
  // Reset window display according to the aspect ratio of remote video.
  window.onresize();
  videoChat = true;
  displayButtons(videoChat);
}

function transitionToWaiting() {
  startTime = endTime = null;
  // Prepare the local video element.
  reattachMediaStream(localVideo, miniVideo);
  miniVideo.style.opacity = 0;
  remoteVideo.style.opacity = 0;
  // Spin the card to show local video (800 ms). Set a timer to detach the
  // remote and PIP video once the transition completes.
  card.style.webkitTransform = 'rotateY(0deg)';
  setTimeout(function() {
    miniVideo.src = '';
    remoteVideo.src = '';
  }, 800);
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
  // When full-screening the canvas we want to avoid the extra spacing
  // introduced by the containing div, but when full-screening the rectangular
  // view we want to keep the full container visible (including e.g. miniVideo).
  var element = event.target.id === 'remoteCanvas' ? event.target : containerDiv;
  element.webkitRequestFullScreen();
}

function noteIceCandidate(location, type) {
  var types = gatheredIceCandidateTypes[location];
  if (!types[type]) {
    types[type] = 1;
  } else {
    ++types[type];
  }
  updateInfoDiv();
}

function getInfoDiv() {
  return document.getElementById("infoDiv");
}

function buildLine(label, value) {
  var columnWidth = 12;
  var line = '';
  if (label) {
    line += label + ':';
    while (line.length < columnWidth) {
      line += ' ';
    }
    if (value) {
      line += value;
    }
  }
  line += '\n';
  return line;
}

function updateInfoDiv() {
  var contents = '<pre>';
  if (pc) {
    // Obtain any needed values from stats.
    var rtt = extractStatAsInt(stats, 'ssrc', 'googRtt');
    var captureStart = extractStatAsInt(stats, 'ssrc',
        'googCaptureStartNtpTimeMs');
    var e2eDelay = computeE2EDelay(captureStart, remoteVideo.currentTime);
    var activeCandPair = getStatsReport(stats, 'googCandidatePair',
        'googActiveConnection', 'true');
    var localAddr, remoteAddr;
    if (activeCandPair) {
      localAddr = activeCandPair.stat('googLocalAddress');
      remoteAddr = activeCandPair.stat('googRemoteAddress');
    }

    // Build the display.
    contents += buildLine('States');
    contents += buildLine('Signaling', pc.signalingState);
    contents += buildLine('Gathering', pc.iceGatheringState);
    contents += buildLine('Connection', pc.iceConnectionState);
    for (var endpoint in gatheredIceCandidateTypes) {
      var types = [];
      for (var type in gatheredIceCandidateTypes[endpoint]) {
        types.push(type + ':' + gatheredIceCandidateTypes[endpoint][type]);
      }
      types.sort();
      contents += buildLine(endpoint, types.join(' '));
    }
    if (localAddr && remoteAddr) {
      contents += buildLine('LocalAddr', localAddr);
      contents += buildLine('RemoteAddr', remoteAddr);
    }
    contents += buildLine();

    contents += buildLine('Stats');
    if (endTime !== null) {
      contents += buildLine('Setup time',
          (endTime - startTime).toFixed(0).toString() + 'ms');
    }
    if (rtt !== null) {
      contents += buildLine('RTT', rtt.toString() + 'ms');
    }
    if (e2eDelay !== null) {
      contents += buildLine('End to end', e2eDelay.toString() + 'ms');
    }
  }
  contents += '</pre>';

  var div = getInfoDiv();
  div.innerHTML = contents;

  for (var msg in infoDivErrors) {
    div.innerHTML += '<p style="background-color: red; color: yellow;">' +
        infoDivErrors[msg] + '</p>';
  }
}

function isInfoDivVisible() {
  return getInfoDiv().style.display === 'block';
}

function showInfoDiv() {
  if (getStatsTimer) {
    throw 'Inconsistent infodiv state';
  }
  var div = getInfoDiv();
  div.style.display = 'block';
  // Start stat updates.
  refreshStats();
  getStatsTimer = setInterval(refreshStats, 1000);
}

function hideInfoDiv() {
  var div = getInfoDiv();
  div.style.display = 'none';
  clearInterval(getStatsTimer);
}

function toggleInfoDiv() {
  if (isInfoDivVisible()) {
    hideInfoDiv();
  } else {
    showInfoDiv();
  }
}

function toggleVideoMute() {
  // Call the getVideoTracks method via adapter.js.
  var videoTracks = localStream.getVideoTracks();

  if (videoTracks.length === 0) {
    trace('No local video available.');
    return;
  }

  trace('Toggling video mute state.');
  var i;
  if (isVideoMuted) {
    for (i = 0; i < videoTracks.length; i++) {
      videoTracks[i].enabled = true;
    }
    trace('Video unmuted.');
  } else {
    for (i = 0; i < videoTracks.length; i++) {
      videoTracks[i].enabled = false;
    }
    trace('Video muted.');
  }

  isVideoMuted = !isVideoMuted;
}

function toggleAudioMute() {
  // Call the getAudioTracks method via adapter.js.
  var audioTracks = localStream.getAudioTracks();

  if (audioTracks.length === 0) {
    trace('No local audio available.');
    return;
  }

  trace('Toggling audio mute state.');
  var i;
  if (isAudioMuted) {
    for (i = 0; i < audioTracks.length; i++) {
      audioTracks[i].enabled = true;
    }
    trace('Audio unmuted.');
  } else {
    for (i = 0; i < audioTracks.length; i++) {
      audioTracks[i].enabled = false;
    }
    trace('Audio muted.');
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
  if (navigator.appVersion.indexOf('Mac') !== -1) {
    hotkey = event.metaKey;
  }
  if (!hotkey) {
    return;
  }
  switch (event.keyCode) {
    case 68:
      toggleAudioMute();
      return false;
    case 69:
      toggleVideoMute();
      return false;
    case 73:
      toggleInfoDiv();
      return false;
    default:
      return;
  }
};

function maybeSetAudioSendBitRate(sdp) {
  if (!audioSendBitrate) {
    return sdp;
  }
  trace('Prefer audio send bitrate: ' + audioSendBitrate);
  return preferBitRate(sdp, audioSendBitrate, 'audio');
}

function maybeSetAudioReceiveBitRate(sdp) {
  if (!audioRecvBitrate) {
    return sdp;
  }
  trace('Prefer audio receive bitrate: ' + audioRecvBitrate);
  return preferBitRate(sdp, audioRecvBitrate, 'audio');
}

function maybeSetVideoSendBitRate(sdp) {
  if (!videoSendBitrate) {
    return sdp;
  }
  trace('Prefer video send bitrate: ' + videoSendBitrate);
  return preferBitRate(sdp, videoSendBitrate, 'video');
}

function maybeSetVideoReceiveBitRate(sdp) {
  if (!videoRecvBitrate) {
    return sdp;
  }
  trace('Prefer video receive bitrate: ' + videoRecvBitrate);
  return preferBitRate(sdp, videoRecvBitrate, 'video');
}

// Adds a b=AS:bitrate line to the m=mediaType section.
function preferBitRate(sdp, bitrate, mediaType) {
  var sdpLines = sdp.split('\r\n');

  // Find m line for the given mediaType.
  var mLineIndex = findLine(sdpLines, 'm=', mediaType);
  if (mLineIndex === null) {
    messageError('Failed to add bandwidth line to sdp, as no m-line found');
    return sdp;
  }

  // Find next m-line if any.
  var nextMLineIndex = findLineInRange(sdpLines, mLineIndex + 1, -1, 'm=');
  if (nextMLineIndex === null) {
    nextMLineIndex = sdpLines.length;
  }

  // Find c-line corresponding to the m-line.
  var cLineIndex = findLineInRange(sdpLines, mLineIndex + 1, nextMLineIndex,
      'c=');
  if (cLineIndex === null) {
    messageError('Failed to add bandwidth line to sdp, as no c-line found');
    return sdp;
  }

  // Check if bandwidth line already exists between c-line and next m-line.
  var bLineIndex = findLineInRange(sdpLines, cLineIndex + 1, nextMLineIndex,
      'b=AS');
  if (bLineIndex) {
    sdpLines.splice(bLineIndex, 1);
  }

  // Create the b (bandwidth) sdp line.
  var bwLine = 'b=AS:' + bitrate;
  // As per RFC 4566, the b line should follow after c-line.
  sdpLines.splice(cLineIndex + 1, 0, bwLine);
  sdp = sdpLines.join('\r\n');
  return sdp;
}

// Adds an a=fmtp: x-google-min-bitrate=kbps line, if videoSendInitialBitrate
// is specified. We'll also add a x-google-min-bitrate value, since the max
// must be >= the min.
function maybeSetVideoSendInitialBitRate(sdp) {
  if (!videoSendInitialBitrate) {
    return sdp;
  }

  // Validate the initial bitrate value.
  var maxBitrate = videoSendInitialBitrate;
  if (videoSendBitrate) {
    if (videoSendInitialBitrate > videoSendBitrate) {
      messageError('Clamping initial bitrate to max bitrate of ' +
          videoSendBitrate + ' kbps.');
      videoSendInitialBitrate = videoSendBitrate;
    }
    maxBitrate = videoSendBitrate;
  }

  var sdpLines = sdp.split('\r\n');

  // Search for m line.
  var mLineIndex = findLine(sdpLines, 'm=', 'video');
  if (mLineIndex === null) {
    messageError('Failed to find video m-line');
    return sdp;
  }

  var vp8RtpmapIndex = findLine(sdpLines, 'a=rtpmap', 'VP8/90000');
  var vp8Payload = getCodecPayloadType(sdpLines[vp8RtpmapIndex]);
  var vp8Fmtp = 'a=fmtp:' + vp8Payload + ' x-google-min-bitrate=' +
      videoSendInitialBitrate.toString() + '; x-google-max-bitrate=' +
      maxBitrate.toString();
  sdpLines.splice(vp8RtpmapIndex + 1, 0, vp8Fmtp);
  return sdpLines.join('\r\n');
}

// Promotes |audioSendCodec| to be the first in the m=audio line, if set.
function maybePreferAudioSendCodec(sdp) {
  if (audioSendCodec === '') {
    trace('No preference on audio send codec.');
    return sdp;
  }
  trace('Prefer audio send codec: ' + audioSendCodec);
  return preferAudioCodec(sdp, audioSendCodec);
}

// Promotes |audioRecvCodec| to be the first in the m=audio line, if set.
function maybePreferAudioReceiveCodec(sdp) {
  if (audioRecvCodec === '') {
    trace('No preference on audio receive codec.');
    return sdp;
  }
  trace('Prefer audio receive codec: ' + audioRecvCodec);
  return preferAudioCodec(sdp, audioRecvCodec);
}

// Sets |codec| as the default audio codec if it's present.
// The format of |codec| is 'NAME/RATE', e.g. 'opus/48000'.
function preferAudioCodec(sdp, codec) {
  var sdpLines = sdp.split('\r\n');

  // Search for m line.
  var mLineIndex = findLine(sdpLines, 'm=', 'audio');
  if (mLineIndex === null) {
    return sdp;
  }

  // If the codec is available, set it as the default in m line.
  var codecIndex = findLine(sdpLines, 'a=rtpmap', codec);
  if (codecIndex) {
    var payload = getCodecPayloadType(sdpLines[codecIndex]);
    if (payload) {
      sdpLines[mLineIndex] = setDefaultCodec(sdpLines[mLineIndex], payload);
    }
  }

  sdp = sdpLines.join('\r\n');
  return sdp;
}

// Adds fmtp param to specified codec in SDP.
function addCodecParam(sdp, codec, param) {
  var sdpLines = sdp.split('\r\n');

  // Find opus payload.
  var index = findLine(sdpLines, 'a=rtpmap', codec);
  var payload;
  if (index) {
    payload = getCodecPayloadType(sdpLines[index]);
  }

  // Find the payload in fmtp line.
  var fmtpLineIndex = findLine(sdpLines, 'a=fmtp:' + payload.toString());
  if (fmtpLineIndex === null) {
    return sdp;
  }

  sdpLines[fmtpLineIndex] = sdpLines[fmtpLineIndex].concat('; ', param);

  sdp = sdpLines.join('\r\n');
  return sdp;
}

// Find the line in sdpLines that starts with |prefix|, and, if specified,
// contains |substr| (case-insensitive search).
function findLine(sdpLines, prefix, substr) {
  return findLineInRange(sdpLines, 0, -1, prefix, substr);
}

// Find the line in sdpLines[startLine...endLine - 1] that starts with |prefix|
// and, if specified, contains |substr| (case-insensitive search).
function findLineInRange(sdpLines, startLine, endLine, prefix, substr) {
  var realEndLine = endLine !== -1 ? endLine : sdpLines.length;
  for (var i = startLine; i < realEndLine; ++i) {
    if (sdpLines[i].indexOf(prefix) === 0) {
      if (!substr ||
          sdpLines[i].toLowerCase().indexOf(substr.toLowerCase()) !== -1) {
        return i;
      }
    }
  }
  return null;
}

// Gets the codec payload type from an a=rtpmap:X line.
function getCodecPayloadType(sdpLine) {
  var pattern = new RegExp('a=rtpmap:(\\d+) \\w+\\/\\d+');
  var result = sdpLine.match(pattern);
  return (result && result.length === 2) ? result[1] : null;
}

// Returns a new m= line with the specified codec as the first one.
function setDefaultCodec(mLine, payload) {
  var elements = mLine.split(' ');
  var newLine = [];
  var index = 0;
  for (var i = 0; i < elements.length; i++) {
    if (index === 3) { // Format of media starts from the fourth.
      newLine[index++] = payload; // Put target payload to the first.
    }
    if (elements[i] !== payload) {
      newLine[index++] = elements[i];
    }
  }
  return newLine.join(' ');
}

// Send a BYE on refreshing or leaving a page
// to ensure the room is cleaned up for the next session.
window.onbeforeunload = function() {
  sendMessage({
    type: 'bye'
  });
};

//Juanes
function onChat(){
  var message_user = document.getElementById("chat").value;
  sendMessage({type: 'chat', message: message_user, userid: usuarioChat});  
}

// Set the video diplaying in the center of window.
window.onresize = function(){
  if (!tablero){
    // Don't letterbox while full-screening, by undoing the changes below.
    if (document.webkitIsFullScreen) {
      containerDiv.style.cssText = 'top: 0px; left: 0px;';
      return;
    }

    var aspectRatio;
    if (remoteVideo && remoteVideo.style.opacity === '1') {
      aspectRatio = remoteVideo.videoWidth / remoteVideo.videoHeight;
    } else if (localVideo && localVideo.style.opacity === '1') {
      aspectRatio = localVideo.videoWidth / localVideo.videoHeight;
    } else {
      return;
    }

    var innerHeight = this.innerHeight;
    var innerWidth = this.innerWidth;
    var videoWidth = innerWidth < aspectRatio * window.innerHeight ?
        innerWidth : aspectRatio * window.innerHeight;
    var videoHeight = innerHeight < window.innerWidth / aspectRatio ?
        innerHeight : window.innerWidth / aspectRatio;
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
  var btnChat, btnTablero, btnScreenSharing, btnVD;
  if (chat == false){
    btnChat = '<input type=\'button\' id=\'chatbtn\' class=\'btn wrtcbtn btn-info\' value=\'Mostrar chat\' onclick=\'showChat()\' />'; 
  } else {
    btnChat = '<input type=\'button\' id=\'chatbtn\' class=\'btn wrtcbtn btn-warning\' value=\'Esconder chat\' onclick=\'hideChat()\' />';
  }
  if (tablero == false){
    btnTablero = '<input type=\'button\' id=\'tablero\' class=\'btn wrtcbtn btn-info\' value=\'Iniciar tablero\' onclick=\'onTablero()\' />';
  } else {
    btnTablero = '<input type=\'button\' id=\'tablero\' class=\'btn wrtcbtn btn-warning\' value=\'Detener tablero\' onclick=\'offTablero()\' />';
  }
  if (screenSharing == false){
    btnScreenSharing = '<input type=\'button\' id=\'screenSharing\' class=\'btn wrtcbtn btn-info\' value=\'Compartir Pantalla\' onclick=\'onScreenSharing()\' />';
  } else {
    btnScreenSharing = '<input type=\'button\' id=\'screenSharing\' class=\'btn wrtcbtn btn-warning\' value=\'Detener Compartir Pantalla\' onclick=\'offScreenSharing()\' />';
  }
  if (vd== true){
    btnVD = '<input type=\'button\' id=\'hangup\' class=\'btn wrtcbtn btn-danger\' value=\'Terminar sesión\' onclick=\'onHangup()\' />';
    videoChat = true;
  } else {
    btnVD = 'Conectando...         ';
    btnTablero = ' ';
    btnScreenSharing = ' ';
    videoChat = false;
  }
  if (tablero == true) {
    setStatus(btnVD  + btnTablero + btnChat);
  } else if (screenSharing == true){
    setStatus(btnVD + btnChat + btnScreenSharing);
  }
  else{
    setStatus(btnVD  + btnTablero + btnChat + btnScreenSharing);
  }
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
        chromeMediaSource: 'screen',
         maxWidth: 1280,
         maxHeight: 720
      }
    }
  }, function(stream) {
    screenSharing = true;
    displayButtons(videoChat);
    sendData('{"fn": "onScreenSharing"}');
    attachMediaStream(miniVideo, stream);
    pc.addStream(stream);
    localScreenStream = stream;
    doCall();
   }, function() {
      console.log('Hay error');
   }
  )
}

function offScreenSharing(){
  pc.removeStream(localScreenStream);
  attachMediaStream(miniVideo, localStream);
  sendData('{"fn": "offScreenSharing"}');
  screenSharing = false;
  displayButtons(videoChat);
  localScreenStream.stop();
}

function offRemoteScreenSharing(){
  attachMediaStream(remoteVideo, remoteStream);
  attachMediaStream(miniVideo, localStream);
  miniVideo.muted = true;
}