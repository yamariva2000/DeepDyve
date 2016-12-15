import logging
import pickle
from gensim.summarization import summarize
import gensim
import psycopg2.extras
from gensim.models.doc2vec import Doc2Vec
from pprint import pprint
from database.rds import conn

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class corpus_reader(object):
    def __init__(self, cursor=None, sql=None, tokens_only=False, raw_text=False,sentences=False):
        self.cursor = cursor
        self.sql = sql
        self.tokens_only = tokens_only
        self.raw_text = raw_text
        self.dict = {}
        self.sentences=sentences


    def stream_sentences(self):

        self.cursor.execute(self.sql)
        for doc in self.cursor:
            id = doc[1]
            #title = doc[1]

            text = doc[2]
            sentences = text.split('.')


            self.dict[line[0]]=line[1]
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
                tags=[title])

class model(object):

    def __init__(self):
        self.model = Doc2Vec(workers=4, iter=10, min_count=10)

    def make_model(self,sentences=False):
        self.sentences=sentences
        sql = 'select permdld,title,body from docs  order by permdld limit 100000'# limit 300'
        reader = corpus_reader(cursor=cursor, sql=sql,sentences=self.sentences)

        if self.sentences:
            self.model.build_vocab(reader.stream_sentences())
            self.model.train(reader.stream_sentences())
        else:
            self.model.build_vocab(reader.stream_docs())
            self.model.train(reader.stream_docs())

        self.model_name='model_sentences_{}_100K'.format(self.sentences)
        self.dict_name='dict_sentences_{}_100K'.format(self.sentences)
        self.model.save(self.model_name)

        with open(self.dict_name,mode='wb') as f:
            pickle.dump(reader.dict,f)

    def load_model(self,model_name=None,dict_name=None):
        self.dict_name=dict_name
        self.model = self.model.load(model_name)
        with open(self.dict_name,mode='r') as f:
            self.dict=pickle.load(f)



    def sim(self,sentence):

        sentence=sentence.split(' ')
        inferred_vector = self.model.infer_vector(sentence)

        # print m.model.docvecs.similarity()

        sims = m.model.docvecs.most_similar(positive=[inferred_vector], topn=10)

        pprint(sims)

        print type(sims)

        for i,j in sims:


            sql2="select permdld,title from docs where title = '{}'".format(i)# for i in sims:
            print sql2
            cursor2.execute(sql2)
            print cursor2.fetchone()





        #     print i[0],m.dict[i[0]]
    #




#sim('nuclear')

#
m=model()
m.make_model(sentences=False)


m.load_model(model_name='model_sentences_False_100K', dict_name='dict_sentences_False_100K')

m.sim('bicycle commuting')

