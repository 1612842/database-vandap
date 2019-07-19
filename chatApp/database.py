import abc
import redis
import uuid
import json
from datetime import datetime
from pprint import pprint
import operator
ABC = abc.ABCMeta('ABC', (object,), {})
import mysql_config

print mysql_config.connectionString

class DatabaseBase(ABC):
    @abc.abstractmethod
    def printType(self):
        pass

    @abc.abstractmethod
    def connect(self):
        pass
        

class MySQLDB(DatabaseBase):
    def printType(self):
        print "MySQL"
    
    def connect(self):
        pass
