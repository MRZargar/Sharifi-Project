from datetime import datetime as time
from enum import Enum, auto
import os

class log():
    full_path = ""

    def __init__(self, full_path):
        self.full_path = full_path
        
        path = os.path.dirname(self.full_path)
        if not os.path.isdir(path):
            os.mkdir(path)

    @property
    def __now(self):
        now = time.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        return now

    def log(self, message, message_type):
        try:
            f = open(self.full_path, 'a')
            L = "[%s] %s >> %s.\n" % (self.__now, str(message_type), message)
            f.write(L)
        except Exception as ex:
            pass
        finally:
            f.close()
    
class messageType(Enum):
    INFO = auto()
    ERROR = auto()

    def __str__(self):
        return self.name