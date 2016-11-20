from gensim import corpora
from nltk.stem import snowball,WordNetLemmatizer
from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize,WordPunctTokenizer,wordpunct_tokenize
from gensim.utils import tokenize
from gensim.parsing.porter import PorterStemmer
import gensim.parsing.preprocessing as pre
import logging
from functools32 import lru_cache
from gensim import models
import psycopg2


def clean_tokens(line):
    wnl = WordNetLemmatizer()
    lemmatize = lru_cache(maxsize=50000)(wnl.lemmatize)
    stop_words = set(stopwords.words('english'))
    line = unicode(line).lower()

    #tokens=pre.preprocess_string(line,filters=[pre.strip_tags]) #,filters=[pre.strip_tags])
    tokens = [i for i in tokenize(line) if i not in stop_words]
    return  [lemmatize(i) for i in tokens]


def make_dict_corpus():

#    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.basicConfig( level=logging.INFO)

    fn='/home/kel/deep.csv'

    dictionary = corpora.Dictionary()

    dictionary = corpora.Dictionary(clean_tokens(i) for i in open(fn))


    once_ids = [tokenid for tokenid, docfreq in (dictionary.dfs).iteritems() if docfreq == 1]
    dictionary.filter_tokens(once_ids)  # remove stop words and words that appear only once
    dictionary.filter_extremes()
    dictionary.compactify()
    dictionary.save('deep.dict')

    corpus=[dictionary.doc2bow(clean_tokens(line)) for line in open(fn)]

    corpora.MmCorpus.serialize('corpus.mm', corpus)


class CorpusMaker(object):

    def __init__(self,file=None,fromDB=True):

        self.file=file
        self.fromDB=fromDB
        if fromDB:
            self.dictionary = corpora.Dictionary(documents=self.iterrecords())
        else:
            self.dictionary=corpora.Dictionary(documents=self.iterlines())
        #print self.dictionary

        once_ids = [tokenid for tokenid, docfreq in (self.dictionary.dfs).iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)  # remove stop words and words that appear only once
        self.dictionary.filter_extremes()
        self.dictionary.compactify()
        #print self.dictionary

    def __iter__(self):
        'corpus yielding bow'
        if self.fromDB:
            for t in self.iterrecords():
                yield self.dictionary.doc2bow(t)
        else:
             for t in self.iterlines():
                yield self.dictionary.doc2bow(t)



    def iterlines(self):
        self.fileobject=open(self.file)

        for line in self.fileobject:
            yield clean_tokens(line)

    def iterrecords(self,size=10):
        conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com', database='deepdyve')
        c= conn.cursor()

        c.execute("select * from docs limit 10")
        while True:
            fetch=c.fetchmany(size)
            if not fetch:
                break
            for line in fetch:
                yield clean_tokens(line)

def create_save_corpus_dict(file):

    corpus=CorpusMaker(file)
    #corpus.dictionary.save('deep.dict')
    #corpora.MmCorpus.serialize('corpus.mm',corpus)

