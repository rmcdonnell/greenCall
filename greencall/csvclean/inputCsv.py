""" Read CSV & write JSON file 

CSV must be in format & strings will be converted to ascii:

| unique id | query |
| int, str  | str   |

Reads in CSV file and assign a unique id to each record. 
Ensure that the entry doesn't contain any garbage.

File size is being limited with QUERY_LIMIT since the Google Custom 
Search API only let's you query 100 items per day. 

Currently only handles comma-delimited files with no quote delims;
header must be present.

"""
import csv
import json
import codecs
import logging

#QUERY_LIMIT = 20

def check_num_cols(row):
    """ Ensure csv is of the format [unique_id, query] """
    if len(row) > 2:
        raise TypeError("Incorrect CSV format, read the docstring")

def read_csv(filepath, QUERY_LIMIT):

    outputdict = {}

    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',',quotechar='"')

        outputdict = {}
        header = True
        row_num = 0
        
        for row in csvreader:

            if row_num > QUERY_LIMIT:
                break

            if header:
                check_num_cols(row)
                header = False

            elif not header:
                outputdict[row[0]] = codecs.encode(row[1])

            else:
                logging.error("review the csv file format")

            # increment row number
            row_num += 1

        csvfile.close()

    logging.info("csv converted to Python dictionary")
    return outputdict

def tojson(filepath, outpath, QUERY_LIMIT):
    """ Write query to JSON format """
    outdict = read_csv(filepath, QUERY_LIMIT)

    with open(outpath, 'w') as outjson:
        json.dump(outdict, outjson)
        outjson.close()

    logging.info("csv file converted to JSON and wrote to disk")
        

        

            





