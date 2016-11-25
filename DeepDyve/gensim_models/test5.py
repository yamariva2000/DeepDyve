from DeepDyve.database.postgres_Deep import IterQuery
from gensim.corpora import Dictionary,MmCorpus
from gensim.models import TfidfModel,LsiModel,LdaModel,HdpModel
from gensim.similarities import Similarity,SparseMatrixSimilarity,MatrixSimilarity
from gensim.utils import tokenize
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.corpus import stopwords

import psycopg2
conn = psycopg2.connect(user='kelster', password='CookieDoge',
                                host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
c=conn.cursor()
 # collect statistics about all tokens

class data(object):
    def __init__(self,  conn = psycopg2.connect(user='kelster', password='CookieDoge',
                                host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve'),
                                sql=None):

        self.cursor=conn.cursor()
        self.sql=sql

        self.wnl=WordNetLemmatizer()
        self.lines=[]
    def tokenize(self,doc):

        return [self.wnl.lemmatize(token) for token in tokenize(text=doc,lowercase=True) if (token not in stopwords.words('english') and len(token)>2)]

    def process(self):
        self.cursor.execute(self.sql)
        for line in self.cursor:
            #print line
            self.lines.append(self.tokenize(line[0]))
        return self.lines


class corpus(object):
    def __init__(self,docs=None,dict=None):
        self.docs=docs
        self.dict=dict

    def __iter__(self):
        for doc in self.docs.__iter__():
            yield self.dict.doc2bow(doc)

    def __len__(self):
        return self.__iter__().__sizeof__()



sql='select authors from docs order by id2 limit 50'

data=data(sql=sql)
docs=data.process()


dict=Dictionary(docs)


singleitems = [k for k, i in dict.dfs.iteritems() if i == 1]

dict.filter_tokens(bad_ids=singleitems)

corpus=corpus(docs,dict)




corpus_tfidf=TfidfModel(corpus=corpus,dictionary=dict)[corpus]

model=LsiModel(corpus=corpus_tfidf,id2word=dict,num_topics=20)



#print model.print_topics()

lsi_corpus=model[corpus_tfidf]

index=MatrixSimilarity(model[corpus])




doc = "heat water"
#print doc
vec_bow = dict.doc2bow(doc.lower().split())
vec_lsi = model[vec_bow] # convert the query to Human computer interactionLSI space
print(vec_lsi)

sims=index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])[:5]


sims_id=[int(i[0]) for i in sims]



print sims_id
print 'matching documents:'

for i in sims_id:

    sql='''

    select id2,title from docs where id2 = {}


    '''.format(i)
    c.execute(sql)

    print c.fetchone()




