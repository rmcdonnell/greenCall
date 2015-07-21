""" Tests for greencall/utils/google.py """

from twisted.trial import unittest

from tests.data.test_value import values
from tests.data.test_api_results import data_11111135, data_11111346

from greencall.utils.google import (define_meta_es_doc,
                                    define_result_es_doc,
                                    GoogleParse)

class TestGoogleParser(unittest.TestCase):
    """ Test parsing functionality for google parser """


    def setUp(self):

        self.valuedict = values
        self.meta_info = ("Mister Grouse","123456789")

        
        self.esformat = {
            "_index": "customsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

        self.es_id = 1
        self.gp = GoogleParse(es_id = 1)

    def tearDown(self):
        pass

    def test_sanity_define_meta_es_doc(self):
        """ Sanity check for data type """

        output = define_meta_es_doc(self.valuedict, self.meta_info)

        self.assertEquals(type(output), dict)

    def test_define_meta_es_doc(self):
        """ Walk through data structure """
        output = define_meta_es_doc(self.valuedict, self.meta_info)

        # account info
        self.assertEquals(output['account_holder'], 'Mister Grouse')
        self.assertEquals(output['account_number'], "123456789")

        # search api info
        self.assertEquals(output['kind'], 'customsearch#search')
        self.assertEquals(output['inputEncoding'], 'utf8')
        self.assertEquals(output['exactTerms'], 'asset')

    def test_sanity_define_result_es_doc(self):
        """ Sanity check for data type """
        output = define_result_es_doc(self.valuedict, self.meta_info, 0)

        self.assertEquals(type(output), dict)

    def test_define_result_es_doc(self):
        """ Walk through data structure """
        output = define_result_es_doc(self.valuedict, self.meta_info, 0)
        
        # account info
        self.assertEquals(output['account_holder'], 'Mister Grouse')
        self.assertEquals(output['account_number'], "123456789")

        # search api info
        self.assertEquals(output['kind'], 'customsearch#search')
        self.assertEquals(output['cx'],
                          '003891126258438650518:fcb7zxrqavu')

    def test_sanity_parse_google_json(self):
        """ Sanity check for data type """
        output = self.gp.parse_google_json(self.valuedict,
                                           self.meta_info,
                                           self.esformat)

        self.assertEquals(type(output), list)

    def test_parse_google_json(self):
        """ Walk through data structure """
        output = self.gp.parse_google_json(self.valuedict,
                                           self.meta_info,
                                           self.esformat)
        
        self.assertEquals(type(output.pop()), dict)

        # account info
        self.assertEquals(output[0]['_source']\
                          ['account_holder'], 'Mister Grouse')
        self.assertEquals(output[0]['_source']\
                          ['account_number'], "123456789")

        # search api info
        self.assertEquals(output[0]['_source']\
                          ['kind'], 'customsearch#search')
        self.assertEquals(output[0]['_source']\
                          ['cx'], '003891126258438650518:fcb7zxrqavu')

        # unique search api info
        self.assertEquals(output[0]['_source']\
                          ['title'],
                          'Google Custom Search - Kelley Mote')

    def test_length_parse_google_json(self):
        output = self.gp.parse_google_json(self.valuedict, self.meta_info,
                                           self.esformat)

        # 11 is 1 meta document & 10 search result documents
        self.assertEquals(len(output), 11)

        
class TestGoogleEsLoader(unittest.TestCase):
    """ Test loading functionality for Google Parser """


    def setUp(self):
        
        #self.valuedict = values
        #self.meta_info = ("Mister Grouse","123456789")

        self.account_11111157 = data_11111135
        self.account_11111143 = data_11111346

        self.resultsdict = {'11111157' : data_11111135,
                            '11111143' : data_11111346 }

        self.accountdict = {'11111157' : ('Mister Grouse', '11111157'),
                            '11111143' : ('Taylor Swift', '11111143')}

        self.esformat = {
            "_index": "customsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

        self.es_id = 1
        self.gp = GoogleParse(es_id = 1)

    def tearDown(self):
        pass

    def test_sanity(self):
        pass

    def test_sanity_create_google_es_docs(self):
        """ Sanity check for data type """
        output = self.gp.create_google_es_docs(self.resultsdict,
                                       self.accountdict,
                                       self.esformat)

        # list items are dicts
        self.assertEquals(type(output), list)
        self.assertEquals(type(output[0]), dict)
        
        # two meta documents & 20 search results
        self.assertEquals(len(output), 22)

    def test_create_google_es_docs(self):
        """ Walk through data structure """
        output = self.gp.create_google_es_docs(self.resultsdict,
                                               self.accountdict,
                                               self.esformat)

        self.assertEquals(output[0]['_index'], 'customsearch')
        self.assertEquals(output[0]['_type'], 'website')

    def test_sanity_update_es_doc_id(self):
        """ Sanity check for data type """
        output = self.gp.update_es_doc_id(self.resultsdict,
                                          self.accountdict,
                                          self.esformat)
        
        self.assertEquals(type(output), list)

    def test_update_es_doc_id(self):
        """ Make sure the ES id is correct """
        output = self.gp.update_es_doc_id(self.resultsdict,
                                          self.accountdict,
                                          self.esformat)

        self.assertEquals(output[12]['_id'], 13)
        self.assertEquals(output[0]['_id'], 1)
        self.assertEquals(output[21]['_id'], 22)
        self.assertEquals(output[15]['_id'], 16)

        

        
                          


    
        
        

    
        
        

