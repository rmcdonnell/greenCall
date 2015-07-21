""" Document parser for Google Custom Search API

I was hoping to have more general API to Elasticsearch document 
converter  but it looks like this will have to be API specific. Make
sure the hyperlinks are formatted as 'RAW'.

Given:

esformat = {
            "_index": "ipythonsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

Create:

<meta info>
{ 'account_holder' : 'Mister Grouse',
  'account_number' : '11111417',
  'kind': 'customsearch#search',
  'template' : 'some link about the custom search engine config',
  'title' : 'Google Custom Search - Mister Grouse',
  'totalResults' : '0',
  'searchTerms': 'Mister Grouse',
  'count': 10,
  'language': 'lang_en',
  'inputEncoding': 'utf8',
  'outputEncoding': 'utf8',
  'safe': 'off',
  'cx': '003891126258438650518:fcb7zxrqavu',
  'filter': '1',
  'exactTerms': 'asset',
  'dateRestrict': "'2012'",
  'searchTime': 0.161848,
  'formattedSearchTime': "0.16",
  'totalResults': '0',
}
  
If at least 1 search result exists then a seperate ES document will
be created for each result. That ES document will be of the form:

<result info>
{ 'account_holder' : 'Mister Grouse',
  'account_number' : '11111417',
  'kind': 'customsearch#search',
  'cx': '003891126258438650518:fcb7zxrqavu',
  'title': 'Mister Grouse eats some cheese',
  'link': 'http://www.yellowpages.com/rio-rancho-nm/mister-grouse',
  'snippet': 'A snippet from the webpage about Mister Grouse'
}

Returns:
  List of dictionaries, containing es document formats with payloads
  of meta or search result information.

"""
import logging
import json
import codecs
from itertools import count

from greencall.utils.loadelastic import read_json


def define_meta_es_doc(valuedict, meta_info):
    """
    Args:
        valuedict: json.loads(pydict[key])
        meta_info: tuple, (account holder, account number)

    Returns:
        dictionary for meta es doc values
    """
    meta_es_doc = {}

    holder, number = meta_info
    
    meta_es_doc['account_holder'] = holder
    meta_es_doc['account_number'] = number
    meta_es_doc['kind'] = valuedict['kind'] 
    # mark as raw
    meta_es_doc['template'] = valuedict['url']['template']
    meta_es_doc['title'] = valuedict['queries']['request'][0]['title']
    meta_es_doc['totalResults'] = valuedict['queries']['request']\
                                  [0]['totalResults']
    meta_es_doc['searchTerms'] = valuedict['queries']['request']\
                                 [0]['searchTerms']
    meta_es_doc['count'] = valuedict['queries']['request'][0]['count']
    meta_es_doc['language'] = valuedict['queries']['request'][0]\
                              ['language']
    meta_es_doc['inputEncoding'] = valuedict['queries']['request']\
                                   [0]['inputEncoding']
    meta_es_doc['outputEncoding'] = valuedict['queries']['request'][0]\
                                    ['outputEncoding']
    meta_es_doc['safe'] = valuedict['queries']['request'][0]['safe']
    meta_es_doc['cx'] = valuedict['queries']['request'][0]['cx']
    meta_es_doc['filter'] = valuedict['queries']['request'][0]['filter']
    meta_es_doc['exactTerms'] = valuedict['queries']['request']\
                                [0]['exactTerms']
    meta_es_doc['dateRestrict'] = valuedict['queries']['request']\
                                  [0]['dateRestrict']
    meta_es_doc['searchTime'] = valuedict['searchInformation']\
                                ['searchTime']
    meta_es_doc['formattedSearchTime'] = valuedict['searchInformation']\
                                         ['formattedSearchTime']
    meta_es_doc['totalResults'] = valuedict['searchInformation']\
                                  ['totalResults']
    
    return meta_es_doc

def define_result_es_doc(valuedict, meta_info, index):
    res_es_doc = {}

    holder, number = meta_info

    res_es_doc['account_holder'] = holder
    res_es_doc['account_number'] = number
    res_es_doc['kind'] = valuedict['kind']
    res_es_doc['cx'] = valuedict['queries']['request'][0]['cx']
    res_es_doc['title'] = valuedict['items'][index]['title']
    res_es_doc['link'] = valuedict['items'][index]['link']
    res_es_doc['snippet'] = valuedict['items'][index]['snippet']

    return res_es_doc

class GoogleParse(object):

    def __init__(self, es_id):
        self.es_id = es_id

    def parse_google_items(self, valuedict, meta_info, esformat):
        index = 0
        parsed = []
        while index < len(valuedict['items']):

            _esformat = esformat.copy()

            _esformat['_source'] = define_result_es_doc(valuedict,
                                                        meta_info, index)

            parsed.append(_esformat)
            index += 1

        return parsed

        

    def parse_google_json(self, valuedict, meta_info, esformat):

        parsed = []
        _esformat = esformat.copy()

        _esformat['_source'] = define_meta_es_doc(valuedict, meta_info)
        
        parsed.append(_esformat)

        if 'items' in valuedict:
            parsed.extend(self.parse_google_items(valuedict,
                                                  meta_info, esformat))
        
        
        return parsed

    def create_google_es_docs(self, resultsdict, accountdict, esformat):
        """
        Args:
          resultsdict: read_json(jsonpath)
          accountdict: read_csv(inputpath)
          esformat: dict, contains index info for ES
        """
        esdocs = []

        for key in resultsdict.keys():
            
            key = codecs.encode(str(key))
        
            _esformat = esformat.copy()
            
            if key in accountdict:

                try:

                    meta_info = (accountdict[key], key)

                    result = json.loads(codecs.encode(resultsdict[key],
                                                      'ascii','ignore'))
                    
                    parsed = self.parse_google_json(result,
                                                    meta_info,
                                                    _esformat)
                    esdocs.extend(parsed)
                    
                except TypeError:
                    logging.error("TypeError: {}".format(key))
        
            else:
                logging.warning("key missing from parsed results: {}"\
                                .format(key))

        return esdocs

    def update_es_doc_id(self, resultsdict, accountdict, esformat):
        """ Updates the es doc id using a generator """
        docs = self.create_google_es_docs(resultsdict, accountdict,
                                          esformat)
        num_docs = len(docs)
        itercount = count(self.es_id)
        docs_ready = []

        for doc in docs:

            _doc = doc.copy()

            _doc['_id'] = itercount.next()
            docs_ready.append(_doc)

        return docs_ready

            

    


            
            

        

    

   


