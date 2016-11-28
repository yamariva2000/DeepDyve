import gensim_pipeline as gs
from gensim.utils import tokenize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from gensim.corpora import Dictionary

def sb(x):
    #
    # token_sentences=[]
    #
    #
    #
    # for sentence in text.split('.'):
    #
    #     tokens = tokenize(sentence, lowercase=True)
    #     tokens = [self.wnl.lemmatize(i) for i in tokens]
    #
    #     token_sentences.append(tokens)
    #
    #
    # dict=Dictionary(token_sentences)
    #
    # corpus=[dict.doc2bow(token_sentence) for token_sentence in token_sentences]
    #
    # print dict
    #
    # print corpus
    #
    #
    #




    b_index= MatrixSimilarity[bodycorpus]

    print sorted(enumerate(b_index[vecbow]), key=lambda x: -x[1])[:10]
