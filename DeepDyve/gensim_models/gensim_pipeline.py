import logging
from gensim_preprocess import process_corpus
from gensim.corpora import MmCorpus,Dictionary
from gensim import models,similarities
from gensim.models import HdpModel,LsiModel,LdaModel
import os
import psycopg2
import pandas as pd
import argparse
import csv
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str,help="choose model i.e. LsiModel")
parser.add_argument('--num_topics', type=int,help="choose number of topics")
parser.add_argument('--distributed', type=bool,help="distributed processing")

parser.add_argument('--num_docs', type=int,help="choose number of docs")
parser.add_argument('--doc_field', type=str,help="choose doc field")
parser.add_argument('--lemmatize', type=bool,help="true for lemmatizing")
parser.add_argument('--extra_id', type=str,help="add extra information for your run")
parser.add_argument('--first_sentences', type=bool,help="get x first sentences")
parser.add_argument('--first_n_sentences', type=int,help="enter number of first sentences")

args = parser.parse_args()

argsdict=args.__dict__




conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')

cursor = conn.cursor( cursor_factory=psycopg2.extras.DictCursor)

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

    def __init__(self,run='',sql=None,modelclass=None,modelparams={},lemmatize=False,first_sentences=False,first_n_sentences=10):

        self.run=run
        self.first_n_sentences=first_n_sentences
        self.first_sentences=first_sentences
        self.prefix=os.getcwd()+'/data/'+run+'_'
        self.modelparams=modelparams
        self.sql=sql
        self.modelclass=modelclass
        self.lemmatize=lemmatize
        self.index=[]

    def make_corpus(self):
        assert self.sql, 'data is missing'
        assert self.run,'run id is missing'

        self.corpus=process_corpus(sql=self.sql,lemmatize=self.lemmatize,first_sentences=self.first_sentences,n_sentences=self.first_n_sentences)


        self.dictionary= self.corpus.dictionary




        self.tfidf_vectorizer = models.TfidfModel(corpus=self.corpus )

        self.index= self.corpus.index


    def save_corpus(self):
        assert self.corpus, 'corpus is not in memory'
        assert self.run, 'run id is missing'
        self.dictionary.save(self.prefix+self.corpus.dictionary.__class__.__name__)

        MmCorpus.serialize(fname=self.prefix+'corpus',corpus=self.corpus)

        self.tfidf_vectorizer.save(self.prefix + self.tfidf_vectorizer.__class__.__name__)
        self.corpus_tfidf=self.tfidf_vectorizer[self.corpus]
        MmCorpus.serialize(fname=self.prefix+'corpus_tfidf',corpus=self.corpus_tfidf)

        with open(self.prefix+'db_index','wb') as f:
            writer =csv.writer(f,delimiter=',')
            writer.writerow(['db_index'])
            for i in self.index:
                writer.writerow([i])

    def get_corpus(self,fname=None):
        if fname:
            self.corpus = MmCorpus(fname)
        return self.corpus

    def get_db_index(self,fname=None):
            df=pd.read_csv(fname)

            self.index=df
            return self.index

    def get_corpus_tfidf(self,fname=None):
        if fname:
            self.corpus_tfidf = MmCorpus(fname=fname)
        return self.corpus_tfidf

    def get_dictionary(self,fname=None):
        if fname:
            self.dictionary=Dictionary.load(fname)
        return self.dictionary

    def get_vectorizer_tfidf(self,fname=None):
        if fname:
            self.tfidf_vectorizer=models.TfidfModel.load(fname=fname)
        return self.tfidf_vectorizer

    def make_model(self):
        assert modelclass, 'modelclass is missing'



        self.model  =  self.modelclass(corpus=self.corpus_tfidf,id2word=self.dictionary,**model_params)


        return self.model

    def save_model(self):
        assert self.model,'no model in memory to save'

        print self.prefix+self.model.__class__.__name__
        self.model.save(self.prefix+self.model.__class__.__name__)



    def get_model(self,fname=None):
        if fname:

            self.model=self.modelclass.load(fname=fname)
        return self.model

    def make_sim_index(self):
        assert self.model,'model is missing'
        assert self.corpus,'corpus is missing'

        self.get_corpus(fname=self.prefix + 'corpus')


        self.index= similarities.MatrixSimilarity(self.model[self.get_corpus(fname=self.prefix+'corpus')])

    def save_sim_index(self):

        self.index.save(self.prefix+'index')

    def get_sim_index(self,fname=None):

        self.index=similarities.MatrixSimilarity.load(fname=fname)
        return self.index

    def make_project(self):
        pipe.make_corpus()
        pipe.save_corpus()
        pipe.make_model()
        pipe.save_model()
        pipe.make_sim_index()
        pipe.save_sim_index()


if __name__ =='__main__':


    modelclass=eval(argsdict['model'])

    model_params={}
    if modelclass.__name__ in ['HdpModel',]:
        pass
    else:
        if argsdict['num_topics']==None:
            model_params['num_topics']=200
        else:
            model_params['num_topics']=argsdict['num_topics']
    print model_params
    #model_params['distributed'] = argsdict['distributed']

    n_docs=argsdict['num_docs']


    if argsdict['doc_field'] == None:
        doc_field='body'
    else:
        doc_field=argsdict['doc_field']

    extra_id=argsdict['extra_id']
    if extra_id==None:
        extra_id=''
    lemmatize=argsdict['lemmatize']

    if argsdict['first_sentences']:
        first_sentences=True




    run=extra_id + doc_field +'_' + modelclass.__name__+'_{}'.format(n_docs)
    sql='select permdld,{} from samples order by permdld limit {}'.format(doc_field,n_docs)

    print sql



    pipe=Pipeline(run=run,sql=sql,modelclass=modelclass,modelparams=model_params,lemmatize=argsdict['lemmatize'],first_sentences=first_sentences,
                  first_n_sentences=argsdict['first_n_sentences'])
    pipe.make_project()


    exit()






