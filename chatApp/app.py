from flask import render_template, request, session, jsonify
from flask_socketio import SocketIO
from random import randrange
from mysql_models import *
import os
import mysql_config
from datetime import datetime
from sqlalchemy import or_,and_
from operator import attrgetter

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
usersOnlineDisplayNames = []
usersOnlineAvatars = []
usersOnlineId = []
usersAll = []
FLASK_DEBUG = True


mysql_config.setup(app)
db.init_app(app)


@app.route('/', methods=["GET", "POST"])

def index():

    currDisplayName = session.get('displayName')
    # if user is not logged in and are coming to the page for the first time, return login page
    if request.referrer is None:
        return render_template('login.html')

    # if user is already logged in, return home page
    if session.get('userid') is not None:
        connectionEvent()
        return render_template('home.html')

    previousPage = request.referrer.replace(request.url_root, '')
    
   
    if previousPage == "register" and request.method == "POST":
        return runRegisterAction()

    if (previousPage == "" or previousPage == "/login") and request.method == "POST":
        return runLoginAction()

    else:
        return "Hello"


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')


@app.route("/chat/<id>",methods=["GET", "POST"])
def chat(id):
    connectionEvent()   
    session['receiverid'] = id
    user = User.query.filter_by(user_id =id).first()
    idreceiver = user.user_id
    idsender = session.get("userid")
    
    session["msgHistory"] = []
    content = {}
    con = db.engine.raw_connection()
    cursor = con.cursor()
    cursor.callproc("getMsg", (idsender, idreceiver))
    for row in cursor.fetchall():
       msg = row[11].replace("\n","")
       msg = msg.encode('utf8')
       author = row[2].replace("\n","")
       author = author.encode('utf8')
       content = {"msg": msg, "sender": author, "avatar": row[4]}
       session["msgHistory"].append(content)
       content = {}

    return render_template('chat.html',chatWithUser=user.display_name, avatarUserChatWith=user.avatar)


@socketio.on('connection event')
def connectionEvent():
    newUserDisplayName = session.get('displayName')
    newUseravatar = session.get('avatar')
    newUserId = session.get('userid')

    User.query.filter_by(user_id =newUserId).update(dict(status =1))
    db.session.commit()

    queryAll = User.query.all();

    usersAll = []
    content = {}
    for result in queryAll:
       content = {'user_id': result.user_id, 'display_name': result.display_name, 'avatar': result.avatar}
       usersAll.append(content)
       content = {}

    onlineAll = User.query.filter_by(status =1).all();
    userOnline = []
    content = {}
    for result in onlineAll:
       content = {'user_id': result.user_id}
       userOnline.append(content)
       content = {}
    socketio.emit('someone connected', (newUserId,newUserDisplayName,userOnline, usersAll))


@socketio.on('disconnect')
def disconnect():
    displayName = session.get("displayName")
    userid = session.get("userid")

    User.query.filter_by(user_id =userid).update(dict(status =0))
    db.session.commit()

    
    indexOfUser = usersOnlineDisplayNames.index(displayName)
    usersOnlineDisplayNames.pop(indexOfUser)
    usersOnlineAvatars.pop(indexOfUser)
    session.pop(app.config['SECRET_KEY'], None)
    session.clear()
    socketio.emit('disconnect event', userid)

@socketio.on('message')
def handleMessage(msg):
    messageAuthor = session.get("displayName")
    userAvatar = session.get('avatar')
    userid = session.get('userid')
    
    receiverid = session.get("receiverid");
    msg = msg.encode('utf8'); 
    newMsg = Message(sender=userid,receiver = receiverid,receiver_type = "U",message_content = msg)
    db.session.add(newMsg)
    db.session.commit()

    socketio.emit("incoming message", (msg, userid,receiverid, userAvatar,messageAuthor))


def runRegisterAction():
    
    username = request.form.get("username").lower()
    displayName = request.form.get("displayName").lower()

    if not checkUsernameUniqueness(username):
        return render_template('register.html', error="That username already exists. Please choose again.")

    if not checkDisplayNameUniqueness(displayName):
        return render_template('register.html', error="That display name already exists. Please choose again.")

    
    password = request.form.get("password")
    newUser = User(username=username, password=password, display_name=displayName, avatar=randrange(1, 15))
    db.session.add(newUser)
    db.session.commit()
    updateSession(user=newUser)
    return render_template('home.html')


def runLoginAction():
    username = request.form.get("username").lower()
    password = request.form.get("password").lower()
    user = User.query.filter_by(username=username).first()

    if user is None or user.password != password:
        return render_template('login.html', error="Incorrect credentials. Please try again.")
    else:
        User.query.filter_by(user_id =user.user_id).update(dict(status =1))
        db.session.commit()
        updateSession(user=user)
        return render_template('home.html')


def checkUsernameUniqueness(username):
    usersWithUsername = User.query.filter_by(username=username).count()
    if usersWithUsername > 0:
        return False
    else:
        return True


def checkDisplayNameUniqueness(displayName):
    usersWithDisplayName = User.query.filter_by(display_name=displayName).count()
    if usersWithDisplayName > 0:
        return False
    else:
        return True


def updateSession(user):
    session['displayName'] = user.display_name
    session['username'] = user.username
    session['userid'] = user.user_id
    session['avatar'] = user.avatar
    
    usersOnlineDisplayNames.append(user.display_name)
    usersOnlineAvatars.append(user.avatar)
    usersOnlineId.append(user.user_id)


if __name__ == '__main__':
    socketio.run(app)