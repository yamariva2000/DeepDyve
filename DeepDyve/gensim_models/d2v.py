
import os
from gensim.models import Doc2Vec
from gensim.models import LsiModel,LdaModel,TfidfModel

from gensim.models.wrappers import DtmModel
import pandas as pd
from gensim.corpora import Dictionary,MmCorpus,csvcorpus
from gensim.matutils import corpus2csc
import logging
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import psycopg2.extras
import nltk
from gensim.summarization.textcleaner import clean_text_by_word
import numpy as np
import gensim
import os
import collections
import smart_open
import random

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')
cursor = conn.cursor( cursor_factory=psycopg2.extras.DictCursor)
cursor2 = conn.cursor( cursor_factory=psycopg2.extras.DictCursor)


def get_first_n_sentences_from_document(text, n=10,returnlist=False):
    text = text.replace('\n', '')

    if n==999:
        text = text.split('.')
    else:
        text = text.split('.')[:n]

    if returnlist:
        return text
    else:
        return '.'.join(text)


def test(cursor,sql):

    cursor.execute(sql)

    text=cursor.next()[2]


    f=text.split('.')

    for i in f:
        print i




class corpus_reader(object):
    def __init__(self,cursor=None,sql=None, tokens_only=False,raw_text=False):
        self.cursor=cursor
        self.sql=sql
        self.tokens_only=tokens_only
        self.raw_text=raw_text
        self.dict={}

    def stream(self):
        self.cursor.execute(self.sql)
        for doc in self.cursor:
            text=doc[2]
            sentences=text.split('.')
            id=doc[0]
            title=doc[1]

            #self.dict[line[0]]=line[1]
            for i in xrange(len(sentences)):
                yield gensim.models.doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(sentences[i]),
                                                           tags=[id,title,i ])

            #
            #
            # if self.raw_text:
            #     pass:
            #     #yield (line[0],sentences)
            #
            # else:
            #     if self.tokens_only:
            #         yield gensim.utils.simple_preprocess(sentences)
            #     else:
            #         yield gensim.models.doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(sentences),tags=[line[0]])

sql='select permdld,title,body from docs order by permdld  limit 300'

reader =corpus_reader(cursor=cursor,sql=sql)


for i in reader.stream():
    print i

assert False




#
model = gensim.models.doc2vec.Doc2Vec( window=16, iter=15,workers=3,dbow_words=1)
# model.build_vocab(reader.stream())
# #
# #
# model.train(reader.stream())
# #
# model.save('./d2v/model')

model=model.load('./d2v/model')

sim={}


inferred_vector = model.infer_vector('blood coagulations')


sims = model.docvecs.most_similar([inferred_vector],topn=5)

for i in sims:
    print i[2]








#
#
#
# inferred_vector = model.infer_vector('parasites')
# #print model.similarity(inferred_vector, inferred_vector)
#
#
#
# sims = model.docvecs.most_similar([inferred_vector],topn=10)
#
# for i in sims:
#
#     print i
#     sql="select permdld,title,body from docs where permdld ='{}'".format(i[0])
#
#     cursor2.execute(sql)
#
#
#
#     print cursor2.fetchone()
#









# print doc.tags[0]     ,sim_dict[doc.tags[0]]
# #
# #
