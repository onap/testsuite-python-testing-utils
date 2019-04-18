import json

from deepdiff import DeepDiff

class JSONUtils:
    """JSONUtils is common resource for simple json helper keywords."""
    
    def json_equals(self, left, right):
        """JSON Equals takes in two strings or json objects, converts them into json if needed and then compares them, returning if they are equal or not."""
        if isinstance(left, basestring):
            left_json = json.loads(left);
        else:
            left_json = left;
        if isinstance(right, basestring):
            right_json = json.loads(right);
        else:
            right_json = right;
            
        ddiff = DeepDiff(left_json, right_json, ignore_order=True);
        if ddiff == {}:
            return True;
        else:
            return False;
        
    def make_list_into_dict(self, listOfDicts, key):
        """ Converts a list of dicts that contains a field that has a unique key into a dict of dicts """
        d = {}
        if isinstance(listOfDicts, list):
            for thisDict in listOfDicts:
                v = thisDict[key]
                d[v] = thisDict
        return d
    
    def find_element_in_array(self, searchedArray, key, value):
        """ Takes in an array and a key value, it will return the items in the array that has a key and value that matches what you pass in """
        elements = [];
        for item in searchedArray:
            if key in item:
                if item[key] == value:
                    elements.append(item);
        return elements;