import abc
import redis
import uuid
import json
from datetime import datetime
from pprint import pprint
import operator
ABC = abc.ABCMeta('ABC', (object,), {})

class DatabaseBase(ABC):
    @abc.abstractmethod
    def printType(self):
        pass

    @abc.abstractmethod
    def connect(self,app):
        pass
        