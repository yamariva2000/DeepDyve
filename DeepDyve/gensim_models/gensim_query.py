from nltk import WordNetLemmatizer
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from gensim.matutils import corpus2csc
import gensim_pipeline as gsp
from gensim.models import LsiModel
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)






class Query(object):

    def __init__(self,name=None, num_docs=None):

        extra,field,model_name=name.split('_')
        self.pipe=gsp.Pipeline(modelclass=eval('gsp.'+model_name))

        self.sim_index=self.pipe.get_sim_index(fname="./data/{}_{}_index".format(name,num_docs))
        self.db_index=self.pipe.get_db_index(fname="./data/{}_{}_db_index".format(name,num_docs))
        self.dict=self.pipe.get_dictionary(fname='./data/{}_{}_Dictionary'.format(name,num_docs))
        #print './data/{}_{}_corpus_tfidf'.format(name,num_docs)
        self.corpus=self.pipe.get_corpus(fname='./data/{}_{}_corpus'.format(name,num_docs))
        self.corpus_tfidf=self.pipe.get_corpus_tfidf(fname='./data/{}_{}_corpus_tfidf'.format(name,num_docs))
        self.model=self.pipe.get_model(fname='./data/{}_{}_{}'.format(name,num_docs,model_name))

    def NMFTrans(self):

        self.n = NMF(n_components=2)

        nmfout=self.n.fit_transform(corpus2csc(self.corpus_tfidf))
        print nmfout.shape

        self.km=KMeans(n_clusters=6 )

        kmout=self.km.fit_transform(self.n)

        print kmout.shape


        return











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


        print 'reduced dimension vector:', vec_bow_reduced

        sims=sorted(enumerate(self.sim_index[vec_bow_reduced]),key=lambda x: -x[1])[:15]


        print 'similarities: ',sims

        sims_id = [int(i[0]) for i in sims]

        print sims_id
        print 'matching documents:'


        for i in sims_id:
            #print i,dbindex.iloc[i]['db_index']
            sql = '''


            select permdld,title from samples where permdld = '{}'

            '''.format(self.db_index.iloc[i]['db_index'])


            a=gsp.IterQuery(sql=sql)

            print list(a.iteritems())


q=Query("lem-firstsent_body_LsiModel",2000)

while True:

    query=raw_input('Enter a query: ')
    if query =='':
        break
    q.query(query)


