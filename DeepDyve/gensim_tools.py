from gensim import corpora, models, similarities
import logging
import data_manage as dm
from psycopg2.extras import DictCursor
from gensim.models import doc2vec

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class DDCorpus(object):
    def __iter__(self):
        cursor







class MyCorpus(object):
    def __init__(self):
        self.cursor = dm.conn.cursor('iterator', cursor_factory=DictCursor)
        self.cursor.execute('SELECT body FROM docs LIMIT 10')
        self.dictionary=corpora.Dictionary(self.cursor)



    def __iter__(self):

        for line in self.cursor:


            # assume there's one document per line, tokens separated by whitespace
            yield str(line) #dictionary.doc2bow(str(line).lower().split())


# friendly=MyCorpus()
#y
# for i in friendly:
#     print i
#

# cursor = dm.conn.cursor('iterator', cursor_factory=DictCursor)
# cursor.execute('SELECT body FROM docs LIMIT 10')

for i in dm.cursor():
    print i


model=doc2vec(dm.cursor,size=100,window=8,min_count=5,workers=4)

model.save('testmodel')

