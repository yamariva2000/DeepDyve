from gensim import corpora, models, similarities
import gensim_pipeline
from gensim_pipeline import IterQuery
from gensim.models import LsiModel



class Query(object):

    def __init__(self,text=None,model=LsiModel):
        self.text=text
        self.model=model.load()






lsi=models.LsiModel.load('model2.lsi')
lda=models.LdaModel.load('model2.lda')

dictionary = corpora.Dictionary.load('deep2.dict')
corpus = corpora.MmCorpus('corpus2.mm') # comes from the first tutorial, "From strings to vectors"


index_lsi=similarities.MatrixSimilarity.load('index2.lsi')
index_lda=similarities.MatrixSimilarity.load('index2.lda')


query='human computer interaction'
vec_bow=dictionary.doc2bow(query.lower().split())
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



sim_lda=sorted(enumerate(index_lda[lda_bow]),key=lambda x: -x[1])[:20]



sql='''

select title,subjects_arr[1] from docs where autoid in {}

'''.format(tuple([str(i[0]) for i in sim_lda]))

print sql
i=IterQuery(sql=sql)


for j in i.iteritems():
    print j


# IterQuery('''
#
#
# select title from docs where autoid in {}
#
#
#
# '''.format()
#           )


#print list(enumerate(sims))








