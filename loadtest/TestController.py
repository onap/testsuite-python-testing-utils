'''
Created on Apr 7, 2017

@author: jf9860
'''
import time
import os
from loadtest.RunEte import RunEte
from loadtest.TestConfig import TestConfig


class TestController(object):
    '''
    classdocs
    '''

    threads = {}
    threadid = 0
    soaksubfolder = 'soak_' + str(os.getpid())

    def __init__(self, options):
        '''
        Constructor
        '''
        self.config = TestConfig(duration=options.duration)        
    
    def execute(self):
        self.starttime = int(round(time.time() * 1000))
        self.endttime = self.starttime + (self.config.duration * 1000)
        currenttime = int(round(time.time() * 1000))
        profileindex = 0
        
        while currenttime < self.endttime:
            if (profileindex >= len(self.config.profile)):
                profileindex = 0
            profile = self.config.profile[profileindex]
            sleeptime = profile[0]
            time.sleep(sleeptime)
            self.schedule(profile)
            profileindex = profileindex + 1
            currenttime = int(round(time.time() * 1000))
        
        for threadname in self.threads:
            print "TestController waiting on " + threadname
            t = self.threads[threadname]
            t.join()
            
    def schedule(self, profile):
        self.remove_completed_threads()
        tests = profile[1]
        for test in tests:
            self.schedule_one(test)
    
    def schedule_one(self, test):                
        self.threadid = self.threadid + 1
        threadname = "RunEte_" + str(self.threadid) 
        ''' test for max threads '''
        t = RunEte(test, self.soaksubfolder)
        t.setName(threadname)
        t.start()
        self.threads[threadname] = t
        
    
    def remove_completed_threads(self):
        toremove = []    
        for threadname in self.threads:
            t = self.threads[threadname]
            if (t.isAlive() == False):
                toremove.append(threadname)
        for threadname in toremove:
            print "Removing " + threadname
            del(self.threads[threadname])