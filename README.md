greencall
=========

Makes asyncronous API requests for various clients. Input a csv file and
the API results will eventually be written to MongoDb. For now, I'm
bypassing MongoDb & writing to disk in a JSON format. This allows us
to bulk load into Elasticsearch. You know, < v1 stuff. 

Uses Python 2.7 & Twisted.

Still building, contributions welcome:

``` Shell
$ git clone <repo>
$ cd greenCall && trial tests/
```

Check out the examples folder for ```okgo.py``` & ```okload.py```

``` Shell
$ cp examples/okload.py .
$ pwd
  /my/home/greenCall
$ python okload.py

```