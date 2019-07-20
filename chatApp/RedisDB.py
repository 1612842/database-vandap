import redis
import uuid
import json
from datetime import datetime
from pprint import pprint
import operator
import database

class RedisDB(database.DatabaseBase):

    def __init__(self):
        self.r = redis.Redis()

    def printType(self):
        print "Redis"

    def connect(self,app):
        try:
            app.config['SECRET_KEY'] = 'hehehehe'
            conn = redis.StrictRedis(
                host='localhost',
                port=6379,
                db=1)
            print conn
            conn.ping()
            self.r =conn
            print 'Connected!'
        except Exception as ex:
            print 'Error:', ex
            exit('Failed to connect, terminating.')

    def insertUser(self,username,password,displayName,avatar):
        key = "users:" + str(uuid.uuid1())
        newUser = {
            "username":username,
            "display_name":displayName,
            "password":password,
            "avatar": avatar,
            "status":0
        }
        self.r.hmset(key,newUser)
        newUser["user_id"] = key
        return newUser

    def insertMsg(self,senderid,receiverid,receivertype, message_content):    
        key = "messages:" + str(uuid.uuid1())
        newMsg = {
            "sender":senderid,
            "receiver":receiverid,
            "receiver_type":receivertype,
            "message_time": str(datetime.now()),
            "message_content":message_content
        }
        self.r.hmset(key,newMsg)    

    def getAllMsg(self):
        for key in self.r.scan_iter("messages:*"):
            print key
            print self.r.hgetall(key)


    def getMsg(self,sender, receiver):
        msgs = []
        content = {}
        for key in self.r.scan_iter("messages:*"):
            data = self.r.hgetall(key)
            senderid = data['sender']
            receiverid = data['receiver']
            content={}
            if (senderid==sender and receiverid==receiver) or (senderid==receiver and receiverid==sender):
                senderInfo = self.r.hgetall(senderid)
                content = {
                    "msg":data['message_content'],
                    "sender":senderInfo['display_name'],
                    "avatar":senderInfo['avatar'],
                    "time":data['message_time']
                }
                msgs.append(content)
        msgs.sort(key = operator.itemgetter('time'), reverse = False)
        return msgs       
        #return msg, sender_name, sender_avatar


    def getAllUser(self):
        res = []
        for key in self.r.scan_iter("users:*"):
            content = self.r.hgetall(key)
            content["user_id"] = key
            res.append(content)
        return res


    def getOnlineUser(self):
        res = []
        for key in self.r.scan_iter("users:*"):
            content = self.r.hgetall(key)
            if (content['status']=='1'):
                content["user_id"] = key
                res.append(content)
        return res
                

    def queryUserWithUsername(self,username):
        for key in self.r.scan_iter("users:*"):
            data = self.r.hgetall(key)
            if (data['username']==username):
                data["user_id"] = key
                return data
        return None
    
    def queryUserWithUserID(self,userid):
        data = self.r.hgetall(userid)
        data["user_id"] = userid
        return data

    def makeUserOnline(self, username):
        for key in self.r.scan_iter("users:*"):
            data = self.r.hgetall(key)
            if (data['username']==username):
                data['status'] = '1'
                self.r.hmset(key,data)

    def makeUserOffline(self, userid):
        data = self.r.hgetall(userid)
        data["status"] = '0'
        self.r.hmset(userid,data)
    
    def isUserNameAlreadyExist(self,username):
        for key in self.r.scan_iter("users:*"):
            data = self.r.hgetall(key)
            if (data['username']==username):
                return True
        return False
    
    def isDisplayNameAlreadyExist(self,username):
        for key in self.r.scan_iter("users:*"):
            data = self.r.hgetall(key)
            if (data['display_name']==username):
                return True
        return False

    def isUserAccountIncorrect(self,username,password):
        user = self.queryUserWithUsername(username)
        if user is None or user["password"] != password:
            return True
        return False

# k = RedisDB()
# data = k.getMsg('users:1786d364-a9f4-11e9-b756-a8a79541af6d','users:e44e71a6-a9f2-11e9-b756-a8a79541af6d')

# data = k.queryUserWithUsername("cong")
# print data['username']