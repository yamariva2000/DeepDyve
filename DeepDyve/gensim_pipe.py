from gensim import corpora
from nltk.stem import snowball,WordNetLemmatizer
from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize,WordPunctTokenizer,wordpunct_tokenize
from gensim.utils import tokenize
from gensim.parsing.porter import PorterStemmer
import gensim.parsing.preprocessing as pre


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
fn='../test.csv'
wnl = WordNetLemmatizer()
dictionary = corpora.Dictionary()
stop_words = set(stopwords.words('english'))

# def process_data(line):
#
#     line=word_tokenize(line)
#
#     PorterStemmer.
#
def clean_tokens(line):

    line = unicode(line).lower()

    tokens=pre.preprocess_string(line) #,filters=[pre.strip_tags])
    #tokens = [i for i in tokenize(line) if i not in stop_words]

    return  tokens #  [wnl.lemmatize(i) for i in tokens]



dictionary = corpora.Dictionary(clean_tokens(i) for i in open(fn))

once_ids = [tokenid for tokenid, docfreq in (dictionary.dfs).iteritems() if docfreq == 1]
dictionary.filter_tokens(once_ids)  # remove stop words and words that appear only once
dictionary.filter_extremes()
dictionary.compactify()
dictionary.save('deep.dict')

corpus=[dictionary.doc2bow(clean_tokens(line)) for line in open(fn)]

corpora.MmCorpus.serialize('corpus.mm', corpus)



# >>> # remove stop words and words that appear only once
# >>> stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
# >>>             if stopword in dictionary.token2id]
# >>> once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
# >>> dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
# >>> dictionary.compactify()  # remove gaps in id sequence after words that were removed
# >>> print(dictionary)
# Dictionary(12 unique tokens)
#
#










exit()

# >>> dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
# >>> # remove stop words and words that appear only once
# >>> stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
# >>>             if stopword in dictionary.token2id]
# >>> once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
# >>> dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
# c.>>> dictionary.compactify()  # remove gaps in id sequence after words that were removed
# >>> print(dictionary)
#
#



