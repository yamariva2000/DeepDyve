from nltk.corpus import stopwords
import psycopg2
import gensim
import logging
import psycopg2.extras
from pprint import pprint
from nltk.stem import WordNetLemmatizer,PorterStemmer
from gensim import utils
from gensim.corpora import MmCorpus,Dictionary
import logging
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
conn_string = "host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com' dbname='deepdyve' user='kelster' password='CookieDoge'"

conn = psycopg2.connect(conn_string)

cursor = conn.cursor( cursor_factory=psycopg2.extras.DictCursor)



class process_corpus(object):

    def __init__(self, sql=None,lemmatize=False):

        self.sql=sql

        self.wordnet=WordNetLemmatizer()
        self.pstemmer=PorterStemmer

        self.dictionary = Dictionary(self.iterrecords())

        print('dictionary before:', self.dictionary.token2id)


        once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)
        self.dictionary.compactify()
        print('dictionary after filtering:', self.dictionary.token2id)

    def  __iter__(self):
        self.cl=0
        for tokens in self.iterrecords():  # generates the document tokens and creates bow using dictionary
            self.cl+=1
            yield self.dictionary.doc2bow(tokens)






    def iterrecords(self): # generates document tokens for the dictionary

        self.index=[]
        cursor.execute(self.sql)
        ct=0


        for doc in cursor:
                self.index.append(doc[0])
                doc=doc[1]
                tokens =utils.tokenize(doc,lowercase=True)

                if self.lemmatize:
                    tokens=[self.wordnet.lemmatize(i) for i in tokens if i not in stopwords.words('english')]
                else:
                    tokens = [self.pstemmer.stem(i) for i in tokens if i not in stopwords.words('english')]

                ct += 1
                yield  tokens # or whatever tokenization suits you

    def __len__(self):
        return self.cl
