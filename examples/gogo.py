import json

from elasticsearch import Elasticsearch
from elasticsearch import helpers


with open('foofighters.json','r') as infile:
    data = json.load(infile)
    infile.close()

es = Elasticsearch()
actions = iter(data)
helpers.bulk(es, actions)


