'''
Created on Apr 7, 2017

@author: jf9860
'''
import time
import os
from loadtest.RunEte import RunEte
from loadtest.TestConfig import TestConfig
import logging

class TestController(object):
    '''
    classdocs
    '''

    threads = {}
    threadid = 0
    soaksubfolder = 'soak_' + str(os.getpid())
    test_number = 0

    def __init__(self, options):
        '''
        Constructor
        '''
        self.config = TestConfig(duration=options.duration, cyclelength=options.cyclelength, json=options.profile)
        logging.info(self.config.to_string())

    def execute(self):
        starttime = time.time()
        endtime = starttime + self.config.duration
        profileindex = 0
        currenttime = time.time()
        logging.info("{}:{}:{}".format(starttime, endtime, currenttime))
        while currenttime < endtime:
            if (profileindex >= len(self.config.profile)):
                profileindex = 0
            profile = self.config.profile[profileindex]
            sleeptime = profile[0]
            currenttime = time.time()
            if ((currenttime + sleeptime) < endtime):
                time.sleep(sleeptime)
                self.schedule(profile)
                profileindex = profileindex + 1
                currenttime = time.time()
            else:
                currenttime = endtime

        for threadname in self.threads:
            logging.info("TestController waiting on " + threadname)
            t = self.threads[threadname]
            t.join()
        logging.info("Soak test completed")

    def schedule(self, profile):
        self.remove_completed_threads()
        tests = profile[1]
        for test in tests:
            self.schedule_one(test)

    def schedule_one(self, test):
        self.test_number = self.test_number + 1
        self.threadid = self.threadid + 1
        threadname = "RunEte_" + str(self.threadid)
        ''' test for max threads '''
        t = RunEte(test, self.soaksubfolder, str(self.test_number))
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
            logging.info("Removing " + threadname)
            del(self.threads[threadname])