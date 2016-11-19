import logging
from gensim import corpora, models, similarities
import gensim_preprocess
import gensim_transform

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
corpus=gensim_preprocess.CorpusMaker('/home/kel/test.csv')
corpus.dictionary.save('deep.dict')
corpora.MmCorpus.serialize('corpus.mm',corpus)


#
# gensim_pipe.make_dict_corpus()
#
#
# gensim_transform.make_models()
#


dictionary = corpora.Dictionary.load('deep.dict')
print dictionary

corpus = corpora.MmCorpus('corpus.mm') # comes from the first tutorial, "From strings to vectors"

print corpus

lsi=models.LsiModel.load('model.lsi')




index = similarities.MatrixSimilarity(lsi[corpus])
#index=similarities.Similarity(output_prefix='./',corpus=lsi[corpus])
index.save('index.lsi')








