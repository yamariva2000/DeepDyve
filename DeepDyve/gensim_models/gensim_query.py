from nltk import WordNetLemmatizer

import gensim_pipeline as gsp
pipe=gsp.Pipeline()

index=pipe.get_sim_index(fname="./data/HdpModel_2000_index")

dbindex=pipe.get_index('./data/HdpModel_2000_db_index')



query = 'my dog dental brushing genes'

wnl=WordNetLemmatizer()

vec_bow=pipe.dictionary.doc2bow([wnl.lemmatize(i) for i in query.lower().split()])

print 'query bow: ' , vec_bow

vec_bow_reduced=pipe.modelclass[vec_bow]
print 'reduced dimension vecctor:', vec_bow_reduced

sims=sorted(enumerate(index[vec_bow_reduced]),key=lambda x: -x[1])[:5]

print 'similarities: ',sims

sims_id = [int(i[0]) for i in sims]

print sims_id
print 'matching documents:'

for i in sims_id:
    sql = '''

    select permdld,title from docs where permdld = {}


    '''.format(dbindex['db_index'].iloc(i))

    a=gsp.IterQuery(sql=sql)

    print list(a.iteritems())







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
