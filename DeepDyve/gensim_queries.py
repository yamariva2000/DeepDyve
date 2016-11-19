import logging
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('deep.dict')
corpus = corpora.MmCorpus('corpus.mm') # comes from the first tutorial, "From strings to vectors"
lsi=models.LsiModel.load('model.lsi')



index = similarities.MatrixSimilarity(lsi[corpus])
        similarities.Similarity()
index.save('index.lsi')








