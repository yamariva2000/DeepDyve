import logging
import pickle

import gensim
import psycopg2.extras
from gensim.models.doc2vec import Doc2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
conn = psycopg2.connect(user='kelster', password='CookieDoge',
                        host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class corpus_reader(object):
    def __init__(self, cursor=None, sql=None, tokens_only=False, raw_text=False):
        self.cursor = cursor
        self.sql = sql
        self.tokens_only = tokens_only
        self.raw_text = raw_text
        self.dict = {}

    def stream_sentences(self):

        self.cursor.execute(self.sql)
        for doc in self.cursor:
            id = doc[0]
            title = doc[1]

            text = title + '. ' + doc[2]
            sentences = text.split('.')


            # self.dict[line[0]]=line[1]
            for i in xrange(len(sentences)):
                if len(sentences[i].split(' ')) > 10:
                    id_string = '{}_{}'.format(id, i)
                    self.dict[id_string] = (id_string, title)
                    yield gensim.models.doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(sentences[i]),
                                                               tags=[id_string])

    def stream_docs(self):

        self.cursor.execute(self.sql)
        for doc in self.cursor:
            text = doc[2]
            #sentences = text.split('.')

            id = doc[0]
            title = doc[1]


            self.dict[id] = (id, title)
            yield gensim.models.doc2vec.TaggedDocument(
                words=gensim.utils.simple_preprocess(text),
                tags=[id])

class model(object):

    def __init__(self):
        self.model = Doc2Vec(workers=3, dm=0, iter=15, dbow_words=1)
    def make_model(self):
        sql = 'select permdld,title,body from sample_1500ea order by permdld'
        reader = corpus_reader(cursor=cursor, sql=sql)

        self.model.build_vocab(reader.stream_docs())
        self.model.train(reader.stream_docs())
        self.model.save('model')
        with open('dict',mode='wb') as f:
            pickle.dump(reader.dict,f)

    def load_model(self):
        self.model = self.model.load('model')
        with open('dict',mode='r') as f:
            self.dict=pickle.load(f)






def sim(sentence):
    sim = {}

    sentence=sentence.split(' ')

    m=model()
    m.load_model()

    inferred_vector = m.model.infer_vector(sentence)

    #print model.docvecs.similarity()

    sims = m.model.docvecs.most_similar([inferred_vector], topn=10)
    print sims
    for i in sims:
        print i[0],m.dict[i[0]]


sim('bicycle')

#
#
#
# inferred_vector = model.infer_vector('parasites')
# #print model.similarity(inferred_vector, inferred_vector)
#
#
#
# sims = model.docvecs.most_similar([inferred_vector],topn=10)
#
# for i in sims:
#
#     print i
#     sql="select permdld,title,body from docs where permdld ='{}'".format(i[0])
#
#     cursor2.execute(sql)
#
#
#
#     print cursor2.fetchone()
#









# print doc.tags[0]     ,sim_dict[doc.tags[0]]
# #
# #
