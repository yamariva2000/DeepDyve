import logging
import gensim_preprocess
from gensim.corpora import MmCorpus,Dictionary
import gensim_transform
import gensim_transform as trans
from gensim import models,similarities

if __name__=='__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # corpus=gensim_preprocess.CorpusMaker(fromDB=True) #('/home/kel/deep.csv')

    #corpus.dictionary.save('deep.dict')
    #MmCorpus.serialize('corpus.mm',corpus)

    trans.make_models()

