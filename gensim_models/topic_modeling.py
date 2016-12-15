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
from gensim.summarization.textcleaner import clean_text_by_word
import numpy as np
from database.rds import conn

cursor = conn.cursor()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class cluster(object):

    def __init__(self):
        prefix='./data/'

        #name="fs-lem__body_LsiModel_26000_"
        name='tx8body_LsiModel_26000_'

        # name="lem-firstsent_body_LsiModel_2000_"

        self.corpus=MmCorpus(fname= prefix + name + 'corpus')
        self.corpus_tfidf=MmCorpus(fname= prefix + name + 'corpus_tfidf')
        self.cpdense = corpus2csc(self.corpus_tfidf)
        self.dictionary=Dictionary.load(fname=prefix+name + "Dictionary")
        self.db=pd.read_csv(prefix+name + 'db_index')




    def KMeansBest(self,matrix,n_clusters=8):
        km = KMeans(n_clusters=n_clusters)


        return km.fit_transform(matrix)




    def KMeansMinInertia(self,matrix):
        import matplotlib
        inertias = []
        max=2
        for clusters in range(1,max):
            print clusters
            km = KMeans(n_clusters=clusters)

            kmout = km.fit_transform(matrix)





            inertias.append(km.inertia_)

        matplotlib.rc('font', **font)

        plt.plot(range(1, max), inertias)
        plt.title('KMeans Elbow',size=20)

        plt.xlabel('N-Doc Clusters',size=16)
        plt.ylabel('Cluster Variance',size=16)
        plt.show()


#lda12=LdaModel(corpus=c.corpus_tfidf,num_topics=12,id2word=c.dictionary)
#
#

c=cluster()

question='human evolution'
vec_bow=c.dictionary.doc2bow(clean_text_by_word(question))

        #vec_bow=self.dict.doc2bow(question.lower().split())

        #print 'question bow: ' , vec_bow

#vec_bow_topics=lda8.get_document_topics(vec_bow)


lda8=LdaModel.load('lda8')

lda8corpus=corpus2csc(lda8[c.corpus]).T

vec_bow_reduced=lda8[vec_bow]

vec_bow_index_gone=[i[1] for i in vec_bow_reduced]


vec




k= KMeans(n_clusters=8)

m=k.fit_transform(lda8corpus)

centroids=k.cluster_centers_

groups=k.predict(lda8corpus)

s=pd.Series(groups)
s.name='group'


df=pd.read_sql('select title,subject1, permdld from sample_1500ea order by permdld',con=conn)

c=pd.concat([df,s],axis=1)




topics =[
'mathematics',
'biology / trials',
'academic publising',
'literature online',
'information technology',
'medicine',
'chemistry',
'healthcare']



sb.heatmap(centroids,xticklabels=topics)
plt.title('Topics',size=20)

plt.xticks(rotation=45,size=15)



plt.show(vec_bow_reduced)







#c.KMeansMinInertia(nplda8)



# lda8=LdaModel(corpus=c.corpus_tfidf,num_topics=8,id2word=c.dictionary)
#lda12=LdaModel(corpus=c.corpus_tfidf,num_topics=12,id2word=c.dictionary)


#
# nmf= NMF(n_components=2)
# words_topics=nmf.fit_transform(X=c.cpdense)
#
# docs_topics=nmf.components_.T
#
# dtm=DtmModel
#
#
#
# sqlget=pd.read_sql('select permdld,title from sample_1500ea order by permdld limit 10',conn)
#
#



lda8[]