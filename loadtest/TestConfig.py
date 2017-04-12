'''
Created on Apr 7, 2017

@author: jf9860
'''
class TestConfig(object):
    '''
    The profile defines a cycle of tests. Each entry is defined as
    [<seconds to wait>, [<list of ete tags to run after the wait]],
    '''
    profile =    [
        [0, ["health"]],
        [5, ["instantiate", "distribute"]],
        [300, ["distribute"]],
        [300, ["distribute"]],
        [300, ["distribute"]],
        [300, ["distribute"]],
        [300, ["distribute"]],
    ]

    duration=10
    cyclelength=60

    def __init__(self, duration=10, cyclelength=1800, json=None):
        '''
        Constructor
        '''
        self.duration = duration
        self.cyclelength = cyclelength
        running_time = 0
        for p in self.profile:
            secs = p[0]
            running_time = running_time + secs
        if (running_time < cyclelength):
            last = cyclelength - running_time
            self.profile.append([last, []])

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


