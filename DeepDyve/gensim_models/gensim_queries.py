from gensim import corpora, models, similarities

import DeepDyve
import gensim_preprocess as pre
from DeepDyve.database import postgres_Deep as query
from DeepDyve.database.data_manage import conn
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




lsi=models.LsiModel.load('model.lsi')
lda=models.LdaModel.load('model.lda')

dictionary = corpora.Dictionary.load('deep.dict')
corpus = corpora.MmCorpus('corpus.mm') # comes from the first tutorial, "From strings to vectors"
index_lsi=similarities.MatrixSimilarity.load('index.lsi')
index_lda=similarities.MatrixSimilarity.load('index.lda')


query='Human computer interaction'
vec_bow=dictionary.doc2bow(pre.clean_tokens(query))
lsi_bow=lsi[vec_bow]
lda_bow=lda[vec_bow]




sim_lsi=sorted(enumerate(index_lsi[lsi_bow]),key=lambda x: -x[1])[:20]


# sql='''select title,sa from docs where
#
#
#    '''
#
# df=pd.read_sql(sql=sql,conn=conn)
#











sim_lda=list(enumerate(index_lda[lda_bow]))



#print list(enumerate(sims))








