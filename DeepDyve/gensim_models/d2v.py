
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

cursor.execute('select body from samples_2000 order by permdld limit 100')
# In[2]:

# Set file names for train and test data
test_data_dir = '{}'.format(os.sep).join([gensim.__path__[0], 'test', 'test_data'])
lee_train_file = test_data_dir + os.sep + 'lee_background.cor'
lee_test_file = test_data_dir + os.sep + 'lee.cor'


# ## Define a Function to Read and Preprocess Text

# Below, we define a function to open the train/test file (with latin encoding), read the file line-by-line, pre-process each line using a simple gensim pre-processing tool (i.e., tokenize text into individual words, remove punctuation, set to lowercase, etc), and return a list of words. Note that, for a given file (aka corpus), each continuous line constitutes a single document and the length of each line (i.e., document) can vary. Also, to train the model, we'll need to associate a tag/number with each document of the training corpus. In our case, the tag is simply the zero-based line number.

# In[3]:

class corpus_reader(object):
    def __init__(self,data=None, tokens_only=False,raw_text=False):
        self.data=data
        self.tokens_only=tokens_only
        self.raw_text=raw_text


    def stream(self):

        for i, line in enumerate(self.data):
            if self.raw_text:
                yield (i,line[0])

        else:
            if self.tokens_only:
                yield gensim.utils.simple_preprocess(line[0])
            else:
                yield gensim.models.doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(line[0]),tags=[i])

    def reset(self):
        self.stream().send('restart')





sql='select permdld,title,body from samples_2000 order by permdld limit 100'
cursor.execute(sql)

reader =corpus_reader(cursor)



model = gensim.models.doc2vec.Doc2Vec(size=70, min_count=2, iter=10)


model.build_vocab(reader.stream())




model.train(reader.stream())


ranks = []
second_ranks = []


train_corpus = (read_corpus(sql))
sim_dict={}
for doc in train_corpus:

    inferred_vector = model.infer_vector(doc.words)

    # print inferred_vector



    sims = model.docvecs.most_similar([inferred_vector], topn=5 )#len(model.docvecs))



    print doc.tags[0], '***',sims
    sim_dict[doc.tags[0]]=sims

    # rank=[i[0] for i in sims].index(doc.tags[0])
    #
    # ranks.append(rank)
    # #print ranks
    #
    # second_ranks.append(sims[1])


# print second_ranks

#print collections.Counter(ranks)  #96% accuracy



doc_id = random.randint(0, len(model.docvecs))

#print doc_id,sims[doc_id]

print doc_id,sim_dict[doc_id]


