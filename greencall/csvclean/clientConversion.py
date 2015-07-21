""" Converts JSON file to client API format, retains unique id """

import json
import codecs
import logging

from greencall.clients.googleSearch import GoogleCustomSearch



class ClientConversion(object):
    """ Converts JSON file to Client API format """

    def __init__(self, clientclass):
        """
        Args:
          clientmethod: method, Client API conversion method
          querystr: str, query string to be converted
        """
        self.convert = clientclass

    def convertString(self, queryString):
        """ Returns client API request format 
        
        Args:
          domethod: method from client class the converts query string

        Returns:
          str, client API request format
        """
        return self.convert.queryString()


def runConversion(jsonpath, secretKey):
    """ Converts JSON file to client API format 

    Args:
      jsonpath: path to JSON file that's been converted from CSV input
      clientclass: class, Client API conversion clas
      domethod: method from client class the converts query string

    Returns:
      Python dictionary that is a valid param for use in crawlah.py
    """
    with open(jsonpath, 'r') as jsonin:
        obs = json.load(jsonin)
        jsonin.close()
        
    for key in obs.keys():

        gcs = GoogleCustomSearch(version = '1',
                filtah = '1',
                #cx = '003891126258438650518:fcb7zxrqavu',
                cx = '003891126258438650518:vevgdf0rorg',
                lr = 'lang_en',
                exactTerms = 'asset',
                q= obs[key],
                dateRestrict = "'2012'",
                secretKey = secretKey,
                uniqueId = key)

        obs[key] = codecs.encode(gcs.queryString())

    return obs
        
        

