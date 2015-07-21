""" Tests for greencall/utils/loadelastic.py """

from twisted.trial import unittest

from greencall.utils.loadelastic import (read_json, convert_content,
                                         load_elastic, map_documents,
                                         ElasticsearchDocument,
                                         prepare_all_documents)

class TestElasticBulkLoad(unittest.TestCase):
    """ Test bulk load for elasticsearch python client """


    def setUp(self):
        self.esformat = {
            "_index": "customsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

        self.results_dict = {"content": "foo", 
          "results": {"result_one": {"persona": "phone",
                                     "personb":  "phone",
                                     "personc":  "phone"
                                    },
                      "result_two": ["thing1",
                                     "thing2",
                                     "thing3"
                                    ],
                      "result_three": "none"
                     },
          "query": ["Taylor Swift", "Bob Dole", "Rocketman"]
        }

        self.account = (123456, "Forrest Gump")

        self.es_id = 1

        self.jsondict = {123456 : {"content": "foo", 
          "results": {"result_one": {"persona": "phone",
                                     "personb":  "phone",
                                     "personc":  "phone"
                                    },
                      "result_two": ["thing1",
                                     "thing2",
                                     "thing3"
                                    ],
                      "result_three": "none"
                     },
          "query": ["Taylor Swift", "Bob Dole", "Rocketman"]
        }}

    def tearDown(self):
        pass

    def test_read_json(self):
        """ not really necessary """
        pass

    def test_convert_content(self):
        """ Ensure that a conversion was run smoothly """
        pass

    def test_load_elastic(self):
        """ make sure schema is interpreted correctly, etc. """
        pass

    def test_elasticsearch_document(self):
        """ Reviewing functionality for Elasticsearch document class """
        ed = ElasticsearchDocument(es_id = 1,
                                   source = {"hello": "world"},
                                   account_number = 123456,
                                   account_holder = "Forrest Gump")

        es_document = ed.esFormatGetter(self.esformat)
        # sanity check
        self.assertTrue(len(es_document) > 0)

        # correct id
        self.assertEquals(es_document["_id"], 1)

        # correct _source payload
        self.assertEquals(es_document["_source"]["hello"], "world")

        # correct account number
        self.assertEquals(es_document["_source"]["account_number"],
                          123456)

        # correct account holder
        self.assertEquals(es_document["_source"]["account_holder"],
                          "Forrest Gump")


    def test_map_documents(self):

        temp = map_documents(self.results_dict, self.esformat,
                             self.account, self.es_id)
        
        # sanity check on list length
        self.assertEquals(len(temp), 9)
        
        # check elasticsearch id
        self.assertEquals(temp[8]["_id"], 9)
        self.assertEquals(temp[7]["_id"], 8)
        self.assertEquals(temp[0]["_id"], 1)

        # check _type
        self.assertEquals(temp[0]["_type"], "website")
        
        # check _index
        self.assertEquals(temp[5]["_index"], "customsearch")

        # check _source
        self.assertEquals(temp[8]["_source"]["content"], "foo")

        # check account info
        self.assertEquals(temp[8]["_source"]["account_number"],
                              123456)
        self.assertEquals(temp[8]["_source"]["account_holder"],
                          "Forrest Gump")       

        
    def test_prepare_all_documents(self):
        """ Test stack of prepared documents for elasticsearch """

        account_no, account_holder = self.account 
        
        temp = prepare_all_documents(jsondict = self.jsondict,
                                     esformat = self.esformat,
                                     accountdict = \
                                     {account_no: account_holder})

        # sanity check, should be 9 documents
        self.assertEquals(len(temp), 9)

        # check data type
        self.assertTrue(type(temp) is list)

        # double check data type
        self.assertEquals(temp[0]["_id"], 1)
        self.assertEquals(temp[0]["_source"]["account_number"],
                          123456)

        

    

        

        
