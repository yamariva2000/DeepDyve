import csv
from gensim.summarization.textcleaner import clean_text_by_word
import seaborn as sb
import matplotlib.pyplot as plt
from gensim import utils
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer,PunktSentenceTokenizer
import nltk
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from gensim.matutils import corpus2csc
from gensim.similarities import Similarity,MatrixSimilarity
from gensim.corpora import Dictionary
import gensim_pipeline as gsp
import numpy as np
from gensim.models import LsiModel,LdaModel,TfidfModel
import logging
import psycopg2

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')

cursor = conn.cursor( cursor_factory=psycopg2.extras.DictCursor)


class Query(object):

    def __init__(self,name=None, num_docs=None,tbl=None):
        print name.split('_')

        field,model_name=name.split('_')

        self.pst=PunktSentenceTokenizer
        self.tbl=tbl
        self.pipe=gsp.Pipeline(modelclass=eval('gsp.'+model_name))
        self.wnl=WordNetLemmatizer()
        self.sim_index=self.pipe.get_sim_index(fname="./data/{}_{}_index".format(name,num_docs))
        self.db_index=self.pipe.get_db_index(fname="./data/{}_{}_db_index".format(name,num_docs))
        self.dict=self.pipe.get_dictionary(fname='./data/{}_{}_Dictionary'.format(name,num_docs))
        self.corpus_tfidf=self.pipe.get_corpus_tfidf(fname='./data/{}_{}_corpus_tfidf'.format(name,num_docs))
        #print './data/{}_{}_corpus_tfidf'.format(name,num_docs)
        self.corpus=self.pipe.get_corpus(fname='./data/{}_{}_corpus'.format(name,num_docs))
        self.model=self.pipe.get_model(fname='./data/{}_{}_{}'.format(name,num_docs,model_name))
        #self.model=self.pipe.get_model(fname='./data/lem-firstsent_body_LsiModel_2000_LsiModel_60_topics')
        #self.sim_raw=MatrixSimilarity(self.corpus)
#         print len(self.dict)
#
#         self.sim_raw=Similarity('/tmp/tst',self.corpus,num_features=len(self.dict)
# )

    def get_results(self,sims_ids,sims_ids_KW=None,save=True,name=None):
        if save:
            self.f=open(name+'.txt','wb')


        for i in xrange(len(sims_ids)):

            print '______________________________________________________________________________________________'
            sql = ''' select permdld,subject1,title,body from {tbl} where permdld = '{permdld}'  '''
            doc_id,similarity=sims_ids[i]
            permdld=self.db_index.iloc[doc_id]['db_index']
            cursor.execute(sql.format(tbl=self.tbl,permdld=permdld))
            permdld,subject,title,body = cursor.fetchone()



            # print 'LSI'


            self.f.write('\n{}\n'.format(title))

            self.f.write( 'subject: {subject} id: {permdld} similarity measure: {similarity:.2f}\n'.format(subject=subject,permdld=permdld,similarity=similarity)
                     )



            self.intradocsim(text=body)
            # doc_id, similarity = sims_ids_KW[i]
            # permdld = self.db_index.iloc[doc_id]['db_index']
            # cursor.execute(sql.format(tbl=self.tbl, permdld=permdld))
            # permdld, subject2, title2, body = cursor.fetchone()
            # print 'KW'
            # print '\n{}'.format(title2)
            #
            # print 'subject: {subject2} document: {permdld} similarity measure: {similarity:.2f}'.format(subject2=subject2,
            #                                                                                            permdld=permdld,
            #                                                                                                similarity=similarity)
            #
            # self.intradocsim(text=body)

            # self.f.write(subject.strip('\"'))
            # self.f.write (title.strip('\"')) #+[subject2.strip('\"')] + [title2.strip('\"')])
            #     # bodytext1 = result1[2]

        if self.f:
            self.f.close()

    def intradocsim(self, text=None):

        sentences=nltk.sent_tokenize(text)
        doc_tokens=[]
        for sentence in sentences:
            sentence_tokens=clean_text_by_word(sentence)
            doc_tokens.append(sentence_tokens)

        doc_dict=Dictionary(doc_tokens)
        doc_corpus=[doc_dict.doc2bow(i) for i in doc_tokens]
        #doc_corpus_tfidf=TfidfModel(doc_corpus,id2word=doc_dict)

        doc_index=MatrixSimilarity(doc_corpus)

        qvect=doc_dict.doc2bow(clean_text_by_word(self.question))



        sims = sorted(enumerate(doc_index[qvect]), key=lambda x: -x[1])[:5]

        self.f.write ('sentence similarity ')
        for i, j in sims:
            self.f.write ('(\n{:.2f}) {}\n'.format(j, sentences[i][:])
                     )
        return



    def query(self,question=None,tbl=None):

        import csv

        #print 'query:  ',question
        self.question=question
        self.vec_bow=self.dict.doc2bow(clean_text_by_word(question))
        #vec_bow=self.dict.doc2bow(question.lower().split())

        #print 'question bow: ' , vec_bow



        vec_bow_reduced=self.model[self.vec_bow]

        if vec_bow_reduced==[]:
            print 'vector is empty'
            return


        #print 'reduced dimension vector:', vec_bow_reduced
        n_returned=10
        sims=sorted(enumerate(self.sim_index[vec_bow_reduced]),key=lambda x: -x[1])[:n_returned]
  #      sims_kw = sorted(enumerate(self.sim_raw[self.vec_bow]), key=lambda x: -x[1])[:n_returned]


        print 'LSI similarities: ',sims
#        print 'KW similarities:',sims_kw
        sims_id = [i for i in sims]
 #       sims_id_kw=[i for i in sims_kw]

        fn=query.replace(' ','_')

        self.get_results(sims_id, save=True,name=fn)



if __name__=='__main__':
    # q=Query("lem-firstsent_body_LsiModel",2000)
    #q=Query("lem-firstsent_body_LsiModel",2000)


    #q=Query('fs-lem__body_LsiModel',26000,tbl='sample_1500ea')
    q=Query('tx8body_LsiModel',26000,tbl='sample_1500ea')
    #q=Query('fs-_body_LsiModel',1927)




    while True:
        print
        query=raw_input('Enter a query: ')
        if query =='':
            break
        q.query(query)






