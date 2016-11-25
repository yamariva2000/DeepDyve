import spacy                         # See "Installing spaCy"
import psycopg2
import unidecode
conn = psycopg2.connect(user='kelster', password='CookieDoge',
                                host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
c=conn.cursor()


class iterdata(object):
    def __init__(self):
        conn= psycopg2.connect(user='kelster', password='CookieDoge',
                            host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
        self.c = conn.cursor()
        self.c.execute('select body from docs order by autoid limit 100 ')

    def __iter__(self):

        yield unicode.encode(self.c.fetchone()[0])



nlp = spacy.load('en')
g=iterdata()
for doc in nlp.pipe(g,batch_size=10000,n_threads=3):
    print doc[:100]

