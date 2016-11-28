import seaborn as sb
import matplotlib.pyplot as plt
from gensim import utils
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from gensim.matutils import corpus2csc
from gensim.similarities import MatrixSimilarity,Similarity
from gensim.corpora import Dictionary
import gensim_pipeline as gsp
import numpy as np
from gensim.models import LsiModel,LdaModel,TfidfModel
import logging
import psycopg2
from gensim_preprocess import get_first_n_sentences_from_document
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')

cursor = conn.cursor( cursor_factory=psycopg2.extras.DictCursor)

def sb(vector=None,text=None):
    wnl=WordNetLemmatizer()
    token_sentences=[]
    split_sentences=text.split('.')
    for sentence in split_sentences:

        tokens = utils.tokenize(sentence, lowercase=True)
        tokens = [wnl.lemmatize(i) for i in tokens]

        token_sentences.append(tokens)


    dict=Dictionary(token_sentences)


    corpus=[dict.doc2bow(token_sentence) for token_sentence in token_sentences]


    index=MatrixSimilarity(corpus=corpus)

    q=utils.tokenize(vector,lowercase=True)
    q=[wnl.lemmatize(i) for i in q]
    q=dict.doc2bow(q)
    print '___________________________________________________________________________________________________________________________________________________________'
    sims=sorted(enumerate(index[q]),key=lambda x: -x[1])[:3]

    #print sims

    for i in sims:

        print '      ',split_sentences[i[0]]



class Query(object):

    def __init__(self,name=None, num_docs=None):

        extra,field,model_name=name.split('_')
        self.pipe=gsp.Pipeline(modelclass=eval('gsp.'+model_name))
        self.wnl=WordNetLemmatizer()
        self.sim_index=self.pipe.get_sim_index(fname="./data/{}_{}_index".format(name,num_docs))
        self.db_index=self.pipe.get_db_index(fname="./data/{}_{}_db_index".format(name,num_docs))
        self.dict=self.pipe.get_dictionary(fname='./data/{}_{}_Dictionary'.format(name,num_docs))
        #print './data/{}_{}_corpus_tfidf'.format(name,num_docs)
        self.corpus=self.pipe.get_corpus(fname='./data/{}_{}_corpus'.format(name,num_docs))
        self.corpus_tfidf=self.pipe.get_corpus_tfidf(fname='./data/{}_{}_corpus_tfidf'.format(name,num_docs))
        self.model=self.pipe.get_model(fname='./data/{}_{}_{}'.format(name,num_docs,model_name))
        #self.model=self.pipe.get_model(fname='./data/lem-firstsent_body_LsiModel_2000_LsiModel_60_topics')
    def NMFTrans(self):

        self.n = NMF(n_components=2)

        self.nmfout=self.n.fit_transform(corpus2csc(self.corpus_tfidf).T)

    def KMeansBest(self):
        self.km = KMeans(n_clusters=7)

        self.kmout = self.km.fit_transform(self.nmfout)

        print self.kmout.shape


    def KMeansMinInertia(self):
        inertias=[]
        for clusters in range(1,21):

            self.km=KMeans(n_clusters=clusters )


            kmout=self.km.fit_transform(self.nmfout)

            inertias.append (self.km.inertia_)

        plt.plot(range(1,21),inertias)
        plt.xlabel('N-word clusters')
        plt.ylabel('Cluster Variance')
        plt.show()



    def query(self,question=None):


        print 'query:  ',question
        wnl=WordNetLemmatizer()

        vec_bow=self.dict.doc2bow([wnl.lemmatize(i) for i in question.lower().split()])
        #vec_bow=self.dict.doc2bow(question.lower().split())

        print 'question bow: ' , vec_bow


        vec_bow_reduced=self.model[vec_bow]

        if vec_bow_reduced==[]:
            print 'vector is empty'
            return


        #print 'reduced dimension vector:', vec_bow_reduced

        sims=sorted(enumerate(self.sim_index[vec_bow_reduced]),key=lambda x: -x[1])[:5]


        #print 'similarities: ',sims

        sims_id = [i for i in sims]

        #print sims_id
        print
        print 'matching documents:'
        print

        for i,j in sims_id:
            print 'document: {} similarity measure {} '.format(i,j)
            #print i,dbindex.iloc[i]['db_index']

            sql = '''


            select permdld,title,body from samples where permdld = '{}'

            '''.format(self.db_index.iloc[i]['db_index'])


            cursor.execute(sql)

            result= cursor.fetchone()
            print '__________________________________________________________________________'
            print ','.join(result[:2])
            a=''.join(result[2])
            sb(query,a)


q=Query("lem-firstsent_body_LsiModel",2000)

while True:
    print
    query=raw_input('Enter a query: ')
    if query =='':
        break
    q.query(query)


