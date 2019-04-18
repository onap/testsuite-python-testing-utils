'''
Created on Apr 7, 2017

@author: jf9860
'''
from threading import Thread
import subprocess
import os
from datetime import datetime
import logging

class RunEte(Thread):
    '''
    classdocs
    '''
    robot_test = ""
    robot_command = "runEteTag.sh"
    soaksubfolder = ""
    test_number =0

    def __init__(self, test_name, soaksubfolder, test_number):
        '''
        Constructor
        '''
        super(RunEte, self).__init__()
        self.robot_test = test_name
        self.soaksubfolder = soaksubfolder
        self.test_number = test_number

    def run(self):
        logging.info("{} ({}) started - {}".format(self.getName(), self.robot_test, str(datetime.now())))
        try:
            ''' Add the '/' here so that the shell doesn't require a subfolder... '''
            env = dict(os.environ, SOAKSUBFOLDER=self.soaksubfolder + "/")
            output = subprocess.check_output(["bash", self.robot_command, self.robot_test, self.test_number], shell=False, env=env)
            logging.info("{} ({}) {}".format(self.getName(), self.robot_test, output))
        except Exception, e:
            logging.error("{} ({}) Unexpected error {}".format(self.getName(), self.robot_test, repr(e)))
        logging.info("{} ({}) ended - {}".format(self.getName(), self.robot_test, str(datetime.now())))
