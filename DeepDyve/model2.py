
import pandas as pd
from data_manage import pd_querydb
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
#import graphlab
import cPickle as pickle
from sklearn.metrics.pairwise import cosine_similarity
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer



class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]




df=pd_querydb('select body from docs limit 1000')



vectorizer=TfidfVectorizer(strip_accents='ascii',stop_words='english',)



vect=vectorizer.fit_transform(df['body'])#.toarray()

print vectorizer.get_feature_names()

assert False



with open('my_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)


while True:
    query=raw_input('Enter Q to quit')
    if query=='Q':
        break

    query='veterinary horse animal'
    query_vec=vectorizer.transform(query)



    similarities=cosine_similarity(query_vec,vect[0,:])

    print similarities










