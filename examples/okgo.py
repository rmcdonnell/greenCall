import json
import codecs
import logging

from twisted.internet import reactor

from greencall.crawlah import getPages
from greencall.utils.utilityBelt import enable_log
from greencall.csvclean.inputCsv import tojson
from greencall.csvclean.clientConversion import (runConversion,
                                                 ClientConversion)
from greencall.clients.googleSearch import GoogleCustomSearch

from examples.secret import secret_key

filepath = 'examples/finance_demo.csv'
outpath = 'examples/finance_demo.json'

#od = read_csv(filepath)
#print od.keys()

##tojson(filepath, outpath)


#gcs = GoogleCustomSearch(version = '1',
#                filtah = '1',
#                cx = '003891126258438650518:fcb7zxrqavu',
#                lr = 'lang_en',
#                exactTerms = 'asset',
#                q='Taylor Swift',
#                dateRestrict = "'2012'",
#                secretKey = 'mcLovin_8_his_fake_id',
#               uniqueId = 12345)


#cc = ClientConversion(GoogleCustomSearch)

#api_request = gcs.queryString()

#print api_request

adict = runConversion(jsonpath=outpath,
                      secretKey= secret_key)

#print len(adict)
#print adict.values()


if __name__ == "__main__":
    enable_log('crawlah')
    gp = getPages(adict)
    gp.start()
    reactor.run()


#if __name__ == '__main__':
#    
#    enable_log('crawlah')
#
#    with open('examples/testkitten.json', 'r') as infile:
#        testkitten = json.load(infile)
#
#    for key in testkitten.keys():
#        testkitten[key] = codecs.encode(testkitten[key])
    

#    logging.info("crawlah STARTED")
#    gp = getPages(testkitten)
#    gp.start()
#    reactor.run()
