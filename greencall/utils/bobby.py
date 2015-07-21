# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:15:52 2015

@author: bmcdonnell
"""

class ApiConversion(object):

  def __init__(self):
    self.documents = []

  def myfunk( self, inHole ):
    """
    a = [];
    b = myfunk(google, a);

    Args:
      inHole: Nested dictionary containing either other dictionaries,
              lists, or strings. Originally set up to parse results from
              the Google Search API

      outHole: list

    Returns:
      List of dictionaries where each dict is mapped to a string
      or list.
    """
    for keys in inHole.keys():
        is_list = isinstance(inHole[keys],list)
        is_dict = isinstance(inHole[keys],dict)
        if is_list:
            element = inHole[keys]
            new_element = {keys:element}
            self.documents.append(new_element)

        if is_dict:
            element = inHole[keys].keys()
            new_element = {keys:element}
            self.documents.append(new_element)
            self.myfunk(inHole[keys])

        if not(is_list or is_dict):
            new_element = {keys:inHole[keys]}
            self.documents.append(new_element)

    return self.documents.sort()
