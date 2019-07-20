from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from mysql_models import *
import database

class MySQLDB(database.DatabaseBase):

    def __init__(self):
        self.connectionString = "mysql+pymysql://root:cong@localhost:3306/demo2"
        self.engine = create_engine(self.connectionString)

    def printType(self):
        print "MySQLDB"

    def connect(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = self.connectionString
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config['SECRET_KEY'] = 'hehehehe'
        db.init_app(app)

    def insertUser(self,username,password,displayName,avatar):
        newUser = User(username=username, password=password, display_name=displayName, avatar=avatar)
        db.session.add(newUser)
        db.session.commit()
        return newUser

    def insertMsg(self,senderid,receiverid,receivertype, message_content):    
        newMsg = Message(sender=senderid,receiver = receiverid,receiver_type = receivertype,message_content = message_content)
        db.session.add(newMsg)
        db.session.commit()

    def getMsg(self,sender, receiver):
        msgsRes = []
        content = {}
        con = db.engine.raw_connection()
        cursor = con.cursor()
        cursor.callproc("getMsg", (sender, receiver))
        for row in cursor.fetchall():
            msg = row[11].replace("\n","")
            msg = msg.encode('utf8')
            author = row[2].replace("\n","")
            author = author.encode('utf8')
            content = {"msg": msg, "sender": author, "avatar": row[4]}
            msgsRes.append(content)
            content = {}
        return msgsRes
        #return msg, sender_name, sender_avatar


    def getAllUser(self):
        res = []
        queryAll = User.query.all();
        content = {}
        for result in queryAll:
            content = {'user_id': result.user_id, 'display_name': result.display_name, 'avatar': result.avatar}
            res.append(content)
            content = {}
        return res

    def getOnlineUser(self):
        onlineAll = User.query.filter_by(status =1).all();
        res = []
        content = {}
        for result in onlineAll:
            content = {'user_id': result.user_id}
            res.append(content)
            content = {}
        return res

    def queryUserWithUsername(self,username):
        data = User.query.filter_by(username=username).first()
        dictData = {
            "user_id":data.user_id,
            "username":data.username,
            "display_name":data.display_name,
            "password":data.password,
            "avatar":data.avatar,
            "status":data.status
        }
        return dictData
    
    def queryUserWithUserID(self, userid):
        data = User.query.filter_by(user_id =userid).first()
        dictData = {
            "user_id":data.user_id,
            "username":data.username,
            "display_name":data.display_name,
            "password":data.password,
            "avatar":data.avatar,
            "status":data.status
        }
        return dictData

    def makeUserOnline(self, username):
        User.query.filter_by(username =username).update(dict(status =1))
        db.session.commit()

    def makeUserOffline(self, userid):
        User.query.filter_by(user_id =userid).update(dict(status =0))
        db.session.commit()
    
    def isUserNameAlreadyExist(self,username):
        usersWithUsername = User.query.filter_by(username=username).count()
        if usersWithUsername > 0:
            return True
        else:
            return False

    def isDisplayNameAlreadyExist(self,displayName):
        usersWithDisplayName = User.query.filter_by(display_name=displayName).count()
        if usersWithDisplayName > 0:
            return True
        else:
            return False

    def isUserAccountIncorrect(self,username,password):
        user = self.queryUserWithUsername(username)
        if user is None or user['password'] != password:
            return True
        return False
