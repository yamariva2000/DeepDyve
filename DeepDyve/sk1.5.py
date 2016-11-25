
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

tf=joblib.load('csr_matrixTF')

tfidf=TfidfTransformer().fit_transform(tf)

joblib.dump(tfidf,tfidf.__class__.__name__+'TFIDF.pkl')
