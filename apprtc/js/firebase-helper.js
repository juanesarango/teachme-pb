var firebaseUrl = 'https://teachmeapp.firebaseio.com';
var	firebaseRef = new Firebase(firebaseUrl);
var chatRef = firebaseRef.child('chat');
var sessionChatRef = chatRef.child(appController.loadingParams_.roomId);

function createChat(idChat) {
	var newChattRef = sessionChatRef.push({
	  from: "Teachme",
	  message: "Welcome"
	});
}

function sendMessage() {
	var name = 'Julian';
  var text = $('#messageInput').val();
  sessionChatRef.push({from: name, message: text});
  $('#messageInput').val('');
}

sessionChatRef.on('child_added', function(snapshot) {
  var message = snapshot.val();
	displayChatMessage(message.from, message.message);
    });
function displayChatMessage(name, message) {
  var nameUl = $('<ul class="list-unstyled text-right"></ul>').append($('<li></li>').text(name)).append($('<li></li>').text(message))
  $('#messagesDiv').append(nameUl);
  $('#messagesDiv')[0].scrollTop = $('#messagesDiv')[0].scrollHeight;
};