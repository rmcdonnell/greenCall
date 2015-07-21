"""
Tests for crawler functionality
"""
import os
import sys
import time

from twisted.trial import unittest
from greencall.crawlah import getPages

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.web.error import Error
from twisted.internet.defer import DeferredList

class TestPagesWithDeferreds(unittest.TestCase):
    """ Test anything from getPages calling a deferred """

    def setUp(self):
        """ getPages() requires a dict """
        self.urls = {'google':"https://www.google.com/",
                     'yahoo': "https://www.yahoo.com/",
                     'cnn': "http://www.cnn.com/",
                     'msnbc': "http://www.msnbc.com/"}
        self.fakes = {'test': "testingOneTwo"}
        # Maximum number or requests deferred
        self.MAX_RUN = 20

        # This many seconds will expire between requests sent
        self.RATE_LIMIT = 0

    def test_getters_pages(self):
        gp = getPages(self.fakes, self.MAX_RUN, self.RATE_LIMIT)
        self.assertTrue(len(gp.book), 1)

    def test_getters_data(self):
        gp = getPages(self.fakes, self.MAX_RUN, self.RATE_LIMIT)
         # test fails because reactor is not running
        self.assertFalse(len(gp.data), 0)
        
    def test_pageCallback(self):
        gp = getPages(self.fakes, self.MAX_RUN, self.RATE_LIMIT)
        self.assertTrue(gp.pageCallback(result='testingOneTwo',
                                        key='test'), 'testingOneTwo')

class TestPagesForMissingValues(unittest.TestCase):
    """ Need to make sure False value is appended correctly to list """

    def setUp(self):
        self.urls = {'google':"https://www.google.com/",
                     'test': "testingOneTwo"}
        
        # Maximum number or requests deferred
        self.MAX_RUN = 20

        # This many seconds will expire between requests sent
        self.RATE_LIMIT = 0


    def test_page_ping(self):
        """ Need internet connectivity for these tests """
        # ping google
        hostname = "google.com"
        response = os.system("ping -c 1 " + hostname)
        # test for successful response
        self.assertEqual(response, 0)        
        
    def test_correct_list(self):
        """ Is False value appended correctly ? """
        gp = getPages(self.urls, self.MAX_RUN, self.RATE_LIMIT)
        gp.start()

        if not reactor.running:
            reactor.run()

        data = gp.data

        self.assertEqual(False, data['test'])
        self.assertEqual(data['test'], False)
        self.assertEqual(type(data['google']), str)
        
        if reactor.running:
            reactor.stop()

    def test_reactor_sanity(self):
        """ Make sure reactor is shut off """
        if reactor.running:
            reactor.stop()

        self.assertFalse(reactor.running)


        
    
    
        
        
