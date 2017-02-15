import uuid
import time
import datetime

class UUID:
    """UUID is a simple library that generates a uuid"""
    
    def generate_UUID(self):
        """generate a uuid"""
        return uuid.uuid4()
    
    def generate_MilliTimestamp_UUID(self):
        """generate a millisecond timestamp uuid"""
        then = datetime.datetime.now()
        return int(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)