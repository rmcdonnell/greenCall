
# coding: utf-8

# # Example of correct bulk upload using python elasticsearch client
# 
# [Reference blog](http://unroutable.blogspot.com/2015/03/quick-example-elasticsearch-bulk-index.html).
# 
# [elasticsearch-py](http://elasticsearch-py.readthedocs.org/en/latest/helpers.html) documentation
# 
# 

# In[16]:

import itertools
import string
from elasticsearch import Elasticsearch,helpers
es = Elasticsearch()


# In[17]:

k = ({'_type':'foo', '_index':'test','letters':''.join(letters)}
     for letters in itertools.permutations(string.letters,2))


# In[18]:

k.next()


# In[19]:

k.next()


# In[20]:

#es.indices.create('test')


# In[21]:

helpers.bulk(es,k)


# In[22]:

es.count(index='test')


# # Modifying the example to fit our use case
# 
# We are going to start by reading the json file returned from our search api

# In[23]:

import json
from elasticsearch import Elasticsearch
from greencall.utils.loadelastic import (read_json, load_elastic,
                                         prepare_all_documents,
                                        map_documents)
from greencall.csvclean.inputCsv import read_csv


# In[24]:

resultspath = 'examples/finance_demo2.json'
esformat = {
            "_index": "customsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

accountdict = 'examples/finance_demo.csv'


# In[25]:

es = Elasticsearch()


# In[26]:

results = read_json(resultspath)


# In[27]:

len(results)


# In[28]:

#actions = prepare_all_documents(results, esformat, accountdict)
for key in results.keys():
    key = int(key)
    print("key: {}, type: {}".format(key, type(key)))


# In[29]:

actions = prepare_all_documents(results, esformat, read_csv(accountdict))


# In[30]:

actions = iter(actions)


# In[31]:

actions.next()


# In[32]:

actions.next()


# In[33]:

actions.next()


# In[34]:

actions.next()


# In[36]:

helpers.bulk(es,actions)


# In[37]:

es.count(index='customsearch')


# In[ ]:



