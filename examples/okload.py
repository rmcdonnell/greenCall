""" Elasticsearch load using Python client & util functions """

import json
import logging

from greencall.utils.loadelastic import read_json, load_elastic

resultspath = 'examples/results.json'

#pd = read_json(resultspath)

load_elastic(resultspath)

