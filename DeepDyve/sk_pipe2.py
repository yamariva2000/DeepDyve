
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,wordpunct_tokenize
from bs4 import BeautifulSoup as bs
from sklearn.externals import joblib
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation,NMF,PCA
import pandas as pd
import psycopg2


tfidf=joblib.load('csr_matrixTFIDF.pkl')


lda=LatentDirichletAllocation(verbose=3)


ldaout=lda.fit_transform(tfidf)




joblib.dump(lda,lda.__class__.__name__+'LDA.pkl')

joblib.dump(ldaout,lda.__class__.__name__+'LDA.pkl')
