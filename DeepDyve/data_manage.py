import json
import os
import csv
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
import unidecode

'''[u'body', u'publisher', u'REFAUTHOR', u'volissue', 'permdld', u'title', u'journal', u'issn', u'a_affiliation', u'REFTITLE', u'REFVOL', u'authors', u'sa', u'id']'''

#conn = psycopg2.connect(dbname='deepdyve', user='postgres', host='localhost')


conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')





c = conn.cursor()


# this function parses the deepdyve textfile and uploads it to a postgreSQL database as a json

def upload_json():
    with open("../Downloads/DeepDyve") as fileobject:
        counter = 0
        for line in fileobject:
            deepid = line[:11].strip()
            rest = (line[11:]).replace("'", "")
            d = json.loads(rest)
            d["permdld"] = deepid
            d = json.dumps(d)

            command = "INSERT INTO docs VALUES({});".format(d)

            command = "INSERT INTO docs VALUES ('" + d + "');"
            command = "INSERT INTO docs (permdld,data)VALUES ('{}','{}');".format(deepid, d)
            c.execute(command)
            counter += 1
            if counter % 1000 == 0:
                print counter
        conn.commit()

def make_file():

        with open("/home/kel/Downloads/DeepDyve") as fileobject:
            counter = 0
            for line in fileobject:
                deepid = line[:11].strip()
                rest = (line[11:]).replace("'", "")
                #rest=unidecode.unidecode(rest)
                d = json.loads(rest)
                d["permdld"] = deepid
                counter+=1
                if counter==5:
                    break


make_file()













def pd_querydb(sql):
    df = pd.read_sql(sql, conn)

    return df


def cursor():

    cursor = conn.cursor('iterarter', cursor_factory=DictCursor)
    cursor.execute('SELECT title FROM docs LIMIT 1000')



    row_count = 0
    for row in cursor:
        row_count += 1
        yield str(row)
        #yield "row: %s    %s\n" % (row_count, row)

