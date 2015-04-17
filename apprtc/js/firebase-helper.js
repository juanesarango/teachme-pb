var firebaseUrl = 'https://teachmeapp.firebaseio.com';
var	firebaseRef = new Firebase(firebaseUrl);
var amOnline = firebaseRef.child('.info/connected');
var userRef = firebaseRef.child('precense/'+ SessionUser.id)
var sessionChatRef = firebaseRef.child('chat/' + appController.loadingParams_.roomId);
var sessionSettingsRef = firebaseRef.child('session/' + appController.loadingParams_.roomId);
var sessionParticipantsRef = sessionSettingsRef.child('participants')
var sessionParticipants = []
var remoteUser = {}

function remoteUserOnline() {
  var spanRemoteUSer = $('#chatUSer2Name');
  spanRemoteUSer.html('<span class="glyphicon glyphicon-user" style="color: green"> </span> ' + remoteUser.name)
}

function remoteUserOffline() {
  var spanRemoteUSer = $('#chatUSer2Name');
  spanRemoteUSer.html('<span class="glyphicon glyphicon-user" style="color: red"> </span> ' + remoteUser.name)
}

/* Precense updater */
amOnline.on('value', function(snapshot) {
  if (snapshot.val()) {
    userRef.onDisconnect().remove();
    sessionParticipantsMeRef = sessionParticipantsRef.child(SessionUser.id);
    sessionParticipantsMeRef.onDisconnect().remove();
    sessionParticipantsMeRef.set({name: SessionUser.name, lastName: SessionUser.lastName});
    userRef.set(true);
  }
});

/* Getting the remote user info */

sessionParticipantsRef.on('value', function(participantsSanpshot) {
  if (remoteUser) {
    var s = participantsSanpshot.val();
    if (!s.hasOwnProperty(remoteUser.id)){
      remoteUserOffline();
    }
  }
  participantsSanpshot.forEach(function(childParticipant) {
    if (childParticipant.key() != SessionUser.id ) {
      remoteUser = childParticipant.val();
      remoteUserOnline();
    }
  });

})

/* Function to send messages */
function sendMessage() {
	var name = SessionUser.name;
  var text = $('#messageInput').val();
  sessionChatRef.push({from: name, message: text});
  $('#messageInput').val('');
}

/* Fucntion that listen if new messages has been added*/
sessionChatRef.on('child_added', function(snapshot) {
  var message = snapshot.val();
	displayChatMessage(message.from, message.message);
});

/*Function to display messages */
function displayChatMessage(name, message) {
  if (name == SessionUser.name){
    var nameUl = $('<ul class="list-unstyled text-right"></ul>').append($('<li class="text-success"></li>').text(name)).append($('<li class="small"></li>').text(message))
  }else{
    var nameUl = $('<ul class="list-unstyled"></ul>').append($('<li class="text-primary"></li>').text(name)).append($('<li class="small"></li>').text(message))
  }
  $('#messagesDiv').append(nameUl);
  $('#messagesDiv')[0].scrollTop = $('#messagesDiv')[0].scrollHeight;
  
};

