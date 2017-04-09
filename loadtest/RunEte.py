'''
Created on Apr 7, 2017

@author: jf9860
'''
from threading import Thread
import subprocess
import sys
import os
from datetime import datetime

class RunEte(Thread):
    '''
    classdocs
    '''
    robot_test = ""
    robot_command = "runEteTag.sh"
    soaksubfolder = ""

    def __init__(self, test_name, soaksubfolder):
        '''
        Constructor
        '''
        super(RunEte, self).__init__()
        self.robot_test = test_name
        self.soaksubfolder = soaksubfolder

        
    def run(self):
        print self.getName() + " started - " + str(datetime.now())
        try:
            ''' Add the '/' here so that the shell doesn't require a subfolder... '''
            env = dict(os.environ, SOAKSUBFOLDER=self.soaksubfolder + "/")
            output = subprocess.check_output(["bash", self.robot_command, self.robot_test], shell=False, env=env)
            print output
        except:
            print("Unexpected error:", sys.exc_info()[0]) 
        print self.getName() + "   ended - " + str(datetime.now())
        