import uuid
import time
import datetime
from robot.api.deco import keyword


class UUIDKeywords(object):
    """ Utilities useful for generating UUIDs """

    def __init__(self):
        super(UUIDKeywords, self).__init__()

    @keyword
    def generate_uuid4(self):
        """generate a uuid"""
        return str(uuid.uuid4())

    @keyword
    def generate_uuid1(self):
        """generate a timestamp uuid"""
        return str(uuid.uuid1())

    @keyword
    def generate_timestamp(self):
        """generate a timestamp"""
        then = datetime.datetime.now()
        return int(time.mktime(then.timetuple()) * 1e3 + then.microsecond / 1e3)
