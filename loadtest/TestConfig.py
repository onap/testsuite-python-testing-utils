'''
Created on Apr 7, 2017

@author: jf9860
'''

class TestConfig(object):
    '''
    classdocs
    '''
    profile =    [
        [0, ["health"]],
        [5, ["health"]],
        [10, ["instantiate"]],
        [10, ["distribute"]],
        [30, ["health", "distribute"]]
    ]

    def __init__(self, duration=10, ):
        '''
        Constructor
        '''
        self.duration = duration
        