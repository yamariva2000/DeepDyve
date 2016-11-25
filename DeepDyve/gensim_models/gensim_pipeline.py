import logging
from gensim_preprocess import process_corpus
from gensim.corpora import MmCorpus,Dictionary
from gensim import models,similarities
import os
from nltk.stem import WordNetLemmatizer
import psycopg2
import csv
import pandas as pd
conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')

cursor = conn.cursor('data', cursor_factory=psycopg2.extras.DictCursor)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class IterQuery(object):

    def __init__(self,size=100,sql=None):
        cursor.execute(sql)
        self.size=size

    def iteritems(self):

        while True:

            fetch = cursor.fetchone()
            if not fetch:
                break
            yield fetch

class Pipeline(object):

    def     __init__(self,run=None,sql=None,modelclass=None,modelparams={}):
        assert modelclass,  'modelclass is missing'
        self.run=run
        self.prefix=os.getcwd()+'/data/'+run+'_'
        self.modelparams=modelparams
        self.sql=sql
        self.modelclass=modelclass

    def make_corpus(self):
        assert self.sql, 'data is missing'
        assert self.run,'run id is missing'

        self.corpus=process_corpus(sql=self.sql)


        self.dictionary= self.corpus.dictionary


        self.tfidf_vectorizer = models.TfidfModel(corpus=self.corpus )

        self.index= pd.DataFrame(self.corpus.index,columns=['db_index',])


    def save_corpus(self):
        assert self.corpus, 'corpus is not in memory'
        assert self.run, 'run id is missing'
        self.dictionary.save(self.prefix+self.corpus.dictionary.__class__.__name__)

        MmCorpus.serialize(fname=self.prefix+'corpus',corpus=self.corpus)

        self.tfidf_vectorizer.save(self.prefix + self.tfidf_vectorizer.__class__.__name__)
        self.corpus_tfidf=self.tfidf_vectorizer[self.corpus]
        MmCorpus.serialize(fname=self.prefix+'corpus_tfidf',corpus=self.corpus_tfidf)

        self.index.to_csv(self.prefix+'db_index','w')

    def get_corpus(self,fname=None):
        if fname:
            self.corpus = MmCorpus(fname)
        return self.corpus

    def get_index(self):
        return self.index

    def get_corpus_tfidf(self,fname):
        if fname:
            self.corpus_tfidf = MmCorpus(self.prefix + 'corpus_tfidf')
        return self.corpus_tfidf

    def get_dictionary(self,fname):
        if fname:
            self.dictionary=Dictionary.load(self.prefix + 'Dictionary')
        return self.dictionary

    def get_vectorizer_tfidf(self,fname):
        if fname:
            self.tfidf_vectorizer=models.TfidfModel.load(self.prefix+models.TfidfModel.__name__)
        return self.tfidf_vectorizer

    def make_model(self):

        print self.modelparams
        self.model  =  self.modelclass(corpus=self.corpus_tfidf,id2word=self.dictionary,**model_params)
        return self.model

    def save_model(self):
        assert self.model,'no model in memory to save'
        self.model.save(self.prefix+self.model.__class__.__name__)

    def get_model(self,fn=None):
        if fn:
            self.model=modelclass.load(fn)
        return self.model

    def make_sim_index(self):
        assert self.model,'model is missing'
        assert self.corpus,'corpus is missing'

        self.get_corpus(fname=self.prefix + 'corpus')


        self.index= similarities.MatrixSimilarity(self.model[self.get_corpus(fname=self.prefix+'corpus')])

    def save_sim_index(self):

        self.index.save(self.prefix+'index')

    def get_sim_index(self,fn=None):
        if fn:
            self.index=similarities.MatrixSimilarity.load(fn)
        return self.index

    def make_project(self):
        pipe.make_corpus()
        pipe.save_corpus()
        pipe.make_model()
        pipe.save_model()
        pipe.make_sim_index()
        pipe.save_sim_index()


if __name__ =='__main__':

    n_docs = 200000
    modelclass=models.LdaModel

    model_params={'num_topics':30,}



    extra_id=''
    run=modelclass.__name__+'_{}'.format(n_docs)

    sql='select permdld,body from docs order by autoid limit {}'.format(n_docs)
    print sql


    pipe=Pipeline(run=run,sql=sql,modelclass=modelclass,modelparams=model_params)
    pipe.make_project()


    exit()








    # corpus=pipe.get_corpus()
    # dictionary=pipe.get_dictionary()
    # tfidf=pipe.get_tfidf()
    # model=pipe.get_model(modelclass=models.LsiModel)
    # # index=pipe.get_index()



    #
    #
    # query = 'my dog dental brushing genes'
    #
    # wnl=WordNetLemmatizer()
    #
    # vec_bow=dictionary.doc2bow([wnl.lemmatize(i) for i in query.lower().split()])
    #
    #
    # assert False
    #

















    #
    #
    #
    #
    #
    #
    # while True:
    #
    #     print '--------------------------------------'
    #
    #     query=raw_input('Enter Query:  ')
    #     if query=='':
    #         break
    #
    #
    #     print query
    #     wnl=WordNetLemmatizer()
    #
    #     vec_bow=dictionary.doc2bow([wnl.lemmatize(i) for i in query.lower().split()])
    #
    #     from nltk.stem import WordNetLemmatizer
    #
    #     vec_bow_reduced=model[vec_bow]
    #     print 'reduced dimension vecctor:',\
    #         vec_bow
    #
    #     sim=sorted(enumerate(pipe.index[vec_bow_reduced]),key=lambda x: -x[1])[:5]
    #
    #     print 'similarities: ',\
    #         sim
    #
    #
    #     sims_id = [int(i[0]) for i in sim]
    #
    #     print sims_id
    #     print 'matching documents:'
    #
    #     for i in sims_id:
    #         sql = '''
    #
    #         select id2,title from docs where id2 = {}
    #
    #
    #         '''.format(i)
    #
    #         a=IterQuery(sql=sql)
    #
    #         print list(a.iteritems())
    #
    #
    #
