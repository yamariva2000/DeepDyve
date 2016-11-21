import cPickle as pickle

import nltk
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from DeepDyve.database.data_manage import pd_querydb


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in nltk.word_tokenize(doc)]




def vectorize(save=False):

    vectorizer = TfidfVectorizer( dtype=np.int32, strip_accents='ascii', stop_words='english',
                                 tokenizer=None)

    vect = vectorizer.fit_transform(df['body']).toarray()



    #print np.array2string(matrix, formatter={'float_kind': '{0:.2f}'.format})

    if save:
        with open('my_vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        with open('my_data.pkl','wb') as f:
            pickle.dump(vect,f)

    return vectorizer,vect,df



def unpickle_vect():

    with open('my_vectorizer.pkl') as f:
        vectorizer=pickle.load(f)

    with open('my_data.pkl') as f:
        vect=pickle.load(f)

    return vectorizer,vect


def similar_docs(df,vect, vectorizer,query=None, index=None, topmost=6):

    if query:

        fquery=vectorizer.fit_transform(query)
        similarities = cosine_similarity(fquery,vect).flatten()
        print '''
        __________________________________________________

        {}
        ___________________________________________________
        '''.format(query)
    else:
        similarities = cosine_similarity(vect[index], vect).flatten()
        print '''
        __________________________________________________
        Index: {}
        Title: {}
        Subjects: {}
        ___________________________________________________
                '''.format(index,df['title'][index],df['sa'][index])

    relateddocs=similarities.argsort()[:-topmost:-1]

    for i in relateddocs:

        print '''
                __________________________________________________
                Index: {}
                Title: {}
                Subjects: {}
                ___________________________________________________
                        '''.format(i, df['title'][i], df['sa'][i])
    return df,relateddocs
query='behavioral science psychology chemistry biology'
df = pd_querydb('select body,title,sa from docs')

df.to_csv('deep')

# vectorizer,vect=unpickle_vect()
# similar_docs(df,vect,vectorizer,index=5)
