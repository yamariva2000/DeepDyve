import psycopg2
from functools32 import lru_cache
from gensim import corpora
from gensim.utils import tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def clean_tokens(line):
    '''from string, produces list of clean tokens '''
    wnl = WordNetLemmatizer()
    lemmatize = lru_cache(maxsize=50000)(wnl.lemmatize)
    stop_words = set(stopwords.words('english'))
    line = unicode(line).lower()
    tokens = [i for i in tokenize(line) if i not in stop_words]
    return [lemmatize(i) for i in tokens]


class CorpusMaker(object):
    '''creates corpus dictionary and bag of words for each document
            uses postgresdb or local file
    '''

    def __init__(self, file=None, fromDB=True):
        self.file = file
        self.fromDB = fromDB
        if fromDB:
            self.dictionary = corpora.Dictionary(documents=self.iterrecords())
        else:
            self.dictionary = corpora.Dictionary(documents=self.iterlines())
        # print self.dictionary

        once_ids = [tokenid for tokenid, docfreq in (self.dictionary.dfs).iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)  # remove stop words and words that appear only once
        self.dictionary.filter_extremes()
        self.dictionary.compactify()
        # print self.dictionary

    def __iter__(self):
        'corpus yielding bow'
        if self.fromDB:
            for t in self.iterrecords():
                yield self.dictionary.doc2bow(t)
        else:
            for t in self.iterlines():
                yield self.dictionary.doc2bow(t)

    def iterlines(self):
        self.fileobject = open(self.file)

        for line in self.fileobject:
            yield clean_tokens(line)

    def iterrecords(self, size=10):
        conn = psycopg2.connect(user='kelster', password='CookieDoge',
                                host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
        c = conn.cursor()

        c.execute("select body from docs order by autoid")
        while True:
            fetch = c.fetchmany(size)
            if not fetch:
                break
            for line in fetch:
                yield clean_tokens(line)
