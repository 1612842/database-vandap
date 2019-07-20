window.onload = function () {

  var socket = io.connect('http://' + document.domain + ':' + location.port, {
    transports: ['websocket']
  });
  var firstConnect = true;
  var myName = "";
  var receiverID=0;
  var myId = 0;


  addSubmitButtonListener(socket);

  socket.on('connect', function () {
    socket.emit('connection event');
  });

  socket.on('incoming message', function (msg, senderid,receiverid, avatar, author) {
    if ((senderid == myId && receiverid == receiverID)||(senderid == receiverID && receiverid == myId)){
      if (senderid == myId) {
        addMessageFromSelf(avatar, author, msg);
      } else {
        addMessageFromOtherUser(avatar, author, msg);
      }
      var height = $('#messages-div').height() + 10000;
      $('#messages-div').scrollTop(height);
      $(".messages").animate({ scrollTop: $(document).height()+height}, "fast");
    }
  })

  var stringPathName = window.location.pathname;
  console.log(stringPathName);


  function displayMessage(msg, author,avatar) {
      if (author == myName) {
        addMessageFromSelf(avatar, author, msg);
      } else {
        addMessageFromOtherUser(avatar, author, msg);
      }
  }

  socket.on('someone connected', function (userid,displayName, usersOnline, usersAll) {

    if (firstConnect) {
      myId = userid;
      myName = displayName;
      console.log(usersOnline);
      for (var i = 0; i < usersAll.length; i++) {
        removeUserToOnlineDiv(usersAll[i].user_id)
      }

      for (var i = 0; i < usersOnline.length; i++) {
        addUserToOnlineDiv(usersOnline[i].user_id)
      }

      for (var i = 0; i < usersAll.length; i++) {
        addUserToAllDiv(usersAll[i].user_id, usersAll[i].display_name, usersAll[i].avatar)
      }
      firstConnect = false;
    } else {
      for (var i = 0; i < usersAll.length; i++) {
        removeUserToOnlineDiv(usersAll[i].user_id)
      }
      for (var i = 0; i < usersOnline.length; i++) {
        addUserToOnlineDiv(usersOnline[i].user_id)
      }
    }

    if (stringPathName.includes("chat")) {
      receiverID=stringPathName.split("/")[2];
      var sessionValue = $("#demoSession").data('value');
      console.log(sessionValue)
      var myObject = eval('(' + sessionValue + ')');
      console.log(myObject);
      $('#messages-div').empty();
      for (i in myObject) {
        console.log(myObject[i]["msg"])
        displayMessage(myObject[i]["msg"],myObject[i]["sender"],myObject[i]["avatar"])
      }
    }
  });

  socket.on('disconnect event', function (userWhoLeft) {
    console.log("disconnection detected")
    $("a[href$='chat/"+userWhoLeft+"'] span.contact-status").removeClass("online")
    //addUserChangeMessage(userWhoLeft, false)
  });

} //end onload

function addSubmitButtonListener(socket) {
  $('#myMessage').on('keydown', function (e) {
    var message = $('#myMessage').val()
    if (e.which === 13 && message != "") {
      socket.emit('message', message);
      $('#myMessage').val('')
    }
  });

  $('#sendButton').on('click', function () {
    var message = $('#myMessage').val()
    if (message != "") {
      socket.emit('message', message);
      $('#myMessage').val('')
    }
  })
}

function addUserChangeMessage(displayName, connectionEvent) {
  var joinedOrLeft;
  (connectionEvent) ? joinedOrLeft = "joined": joinedOrLeft = "left";
  $("#messages-div").append('<div class = "user-joined-message">' +
    displayName + " has " + joinedOrLeft + " the room. </div>")
}

function addMessageFromSelf(avatar, author, msg) {
  $("#messages-div").append('<li class="replies"><img src="/static/images/jeff' + avatar + '.jpg"/><p>'+msg+'</p></li>'
  )
};


function addMessageFromOtherUser(avatar, author, msg) {
  $("#messages-div").append('<li class="sent"><img src="/static/images/jeff' + avatar + '.jpg"/><p>'+msg+'</p></li>')
};

function addUserToOnlineDiv(userid) {
  $("a[href$='chat/"+userid+"'] span.contact-status").addClass("online")
}

function removeUserToOnlineDiv(userid) {
  $("a[href$='chat/"+userid+"'] span.contact-status").removeClass("online")
}

function addUserToAllDiv(userid, displayName, avatar) {
  $("#all-users-div").append(
    '<li class="contact active"><a href="/chat/'+userid+'"><div class="wrap"><span class="contact-status"></span><img src="/static/images/jeff'+avatar+
    '.jpg"/><div class="meta"><p class="name">'+displayName+'</p><p class="preview">&nbsp;</p></div></div></a></li>');

    
}