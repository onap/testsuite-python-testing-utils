'''
Created on Apr 7, 2017

@author: jf9860
'''
import json

class TestConfig(object):
    '''
    The profile defines a cycle of tests. Each entry is defined as
    [<seconds to wait>, [<list of ete tags to run after the wait]],
    '''
    profile =    [
        [0, ["health"]],
    ]

    duration=10
    cyclelength=60

    def __init__(self, duration=None, cyclelength=None, json=None):
        '''
        Constructor
        '''
        if (json != None):
            self.parseConfig(json)
        if (duration != None):
            self.duration = duration
        if (cyclelength != None):
            self.cyclelength = cyclelength
        running_time = 0
        for p in self.profile:
            secs = p[0]
            running_time = running_time + secs
        if (running_time < self.cyclelength):
            last = self.cyclelength - running_time
            self.profile.append([last, []])

    def parseConfig(self, fileName):
        with open(fileName) as data_file:
            config = json.load(data_file)
        self.profile = config["profile"]
        self.cyclelength = config["cyclelength"]
        self.duration = config["duration"]


    def to_string(self):
        pstring = 'Cycle length is {} seconds'.format(self.cyclelength)
        pstring = '{}\nDuration is {} seconds'.format(pstring, self.duration)
        running_time = 0
        for p in self.profile:
            secs = p[0]
            running_time = running_time + secs
            for ete in p[1]:
                pstring = "{0}\n{1:08d} : {2:08d} : {3}".format(pstring, secs, running_time, ete)
            if (len(p[1]) == 0):
                pstring = "{0}\n{1:08d} : {2:08d} : {3}".format(pstring, secs, running_time, "")
        return pstring


