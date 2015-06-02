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
      // error    == null || 'permission-denied' || 'not-installed' || 'installed-disabled' || 'not-chrome'
      // sourceId == null || 'string' || 'firefox'
      
      if(sourceId && sourceId != 'firefox') {
          screen_constraints = {
              video: {
                  mandatory: {
                      chromeMediaSource: 'screen',
                      maxWidth: 1920,
                      maxHeight: 1080,
                      minAspectRatio: 1.77
                  }
              }
          };

          if (error === 'permission-denied') return alert('Permission is denied.');
          if (error === 'not-chrome') return alert('Please use chrome.');

          if (!error && sourceId) {
              screen_constraints.video.mandatory.chromeMediaSource = 'desktop';
              screen_constraints.video.mandatory.chromeMediaSourceId = sourceId;
          }
      }

      navigator.getUserMedia = navigator.mozGetUserMedia || navigator.webkitGetUserMedia;
      navigator.getUserMedia(screen_constraints, function (stream) {
        screenSharing = true;
        sendData('{"fn": "onScreenSharing"}');
        pcClient_.addStream(stream);
        localScreenStream = stream;
        doCall();
        attachMediaStream(miniVideo, localScreenStream);
      }, function (error) {
          console.error(error);
      });
  });
}
      

function toggleScreenSharing(){
  if (screenSharing){
    offScreenSharing();
  }else{
    onScreenSharing();
  }
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