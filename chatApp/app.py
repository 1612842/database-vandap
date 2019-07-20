from flask import render_template, request, session, jsonify
from flask_socketio import SocketIO
from random import randrange
from mysql_models import *
import os
from datetime import datetime
from sqlalchemy import or_,and_
from operator import attrgetter
from MySQLDB import *
from RedisDB import *

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

usersAll = []
FLASK_DEBUG = True


databaseHelper = RedisDB()
databaseHelper.connect(app)

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
    
    user = databaseHelper.queryUserWithUserID(id)
    
    idreceiver = user['user_id']
    idsender = session.get("userid")
    
    session["msgHistory"] = databaseHelper.getMsg(idsender,idreceiver)

    return render_template('chat.html',chatWithUser=user['display_name'], avatarUserChatWith=user['avatar'])


@socketio.on('connection event')
def connectionEvent():
    newUserDisplayName = session.get('displayName')
    newUsername = session.get('username')
    newUseravatar = session.get('avatar')
    newUserId = session.get('userid')

    databaseHelper.makeUserOnline(newUsername)

    usersAll = databaseHelper.getAllUser()
    
    userOnline = databaseHelper.getOnlineUser()
    
    socketio.emit('someone connected', (newUserId,newUserDisplayName,userOnline, usersAll))


@socketio.on('disconnect')
def disconnect():
    displayName = session.get("displayName")
    userid = session.get("userid")

    databaseHelper.makeUserOffline(userid)
   
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
    
    databaseHelper.insertMsg(userid, receiverid,"U",msg)

    socketio.emit("incoming message", (msg, userid,receiverid, userAvatar,messageAuthor))


def runRegisterAction():
    
    username = request.form.get("username").lower()
    displayName = request.form.get("displayName").lower()

    if databaseHelper.isUserNameAlreadyExist(username):
        return render_template('register.html', error="That username already exists. Please choose again.")

    if databaseHelper.isDisplayNameAlreadyExist(displayName):
        return render_template('register.html', error="That display name already exists. Please choose again.")

    
    password = request.form.get("password")
    newUser = databaseHelper.insertUser(username,password,displayName,randrange(1, 15))
    updateSession(user=newUser)
    return render_template('home.html')


def runLoginAction():
    username = request.form.get("username").lower()
    password = request.form.get("password").lower()
    user = databaseHelper.queryUserWithUsername(username)
    
    if databaseHelper.isUserAccountIncorrect(username,password):
        return render_template('login.html', error="Incorrect credentials. Please try again.")
    else:
        databaseHelper.makeUserOnline(user['username'])
        updateSession(user=user)
        return render_template('home.html')

def updateSession(user):
    session['displayName'] = user['display_name']
    session['username'] = user['username']
    session['userid'] = user['user_id']
    session['avatar'] = user['avatar']
    


if __name__ == '__main__':
    socketio.run(app)