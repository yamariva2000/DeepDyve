
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



conn = psycopg2.connect(user='kelster', password='CookieDoge',host='kelgalvanize.cohsvzbgfpls.us-west-2.rds.amazonaws.com',database='deepdyve')
# dict_cur.execute("SELECT body FROM docs order by id2 limit 100")
#
# rec=dict_cur.fetchone()





class nltk_tokenizer_stemmer(object):
    def __init__(self,text):
        self.wnl=WordNetLemmatizer()
        self.text=text
    def __iter__(self):

        for word in word_tokenize(self.text):

            yield self.wnl.lemmatize(word)


df=pd.read_sql(sql='select body from docs limit 10000',con=conn)


vectorizer=CountVectorizer(stop_words=stopwords.words('english'),tokenizer=nltk_tokenizer_stemmer)

tf=vectorizer.fit_transform(df['body'])

joblib.dump(tf,tf.__class__.__name__+'TF.pkl')







