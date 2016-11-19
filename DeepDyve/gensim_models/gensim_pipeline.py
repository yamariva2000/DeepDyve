import logging
import gensim_preprocess
from gensim.corpora import MmCorpus
import gensim_transform


if __name__=='__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus=gensim_preprocess.CorpusMaker('/home/kel/deep.csv')
    corpus.dictionary.save('deep.dict')
    MmCorpus.serialize('corpus.mm',corpus)
