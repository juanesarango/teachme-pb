function onScreenSharing(){
  // navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.getUserMedia;
  // navigator.getUserMedia({
  //   video: {
  //     mandatory: {
  //       chromeMediaSource: 'screen',
  //        maxWidth: 1280,
  //        maxHeight: 720
  //     }
  //   }
  // }, function(stream) {
    // screenSharing = true;
    // displayButtons(videoChat);
    // sendData('{"fn": "onScreenSharing"}');
    // attachMediaStream(miniVideo, stream);
    // pc.addStream(stream);
    // localScreenStream = stream;
    // doCall();
  //  }, function() {
  //     console.log('Hay error');
  //  }
  // )
  getScreenId(function (error, sourceId, screen_constraints) {
    navigator.getUserMedia = navigator.mozGetUserMedia || navigator.webkitGetUserMedia;
    navigator.getUserMedia(screen_constraints, function (stream) {
      screenSharing = true;
      displayButtons(videoChat);
      sendData('{"fn": "onScreenSharing"}');
      pc.addStream(stream);
      localScreenStream = stream;
      doCall();
      attachMediaStream(miniVideo, localScreenStream);
    }, function (error) {
        console.error(error);
    });
});
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
  remoteStream = pc.getRemoteStreams()[0];
  attachMediaStream(remoteVideo, remoteStream);
  attachMediaStream(miniVideo, localStream);
  miniVideo.muted = true;
}