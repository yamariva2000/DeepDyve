import logging
import gensim_preprocess
from gensim.corpora import MmCorpus,Dictionary
# import gensim_transform
# import gensim_transform as trans
from gensim import models,similarities
import gensim

from DeepDyve.gensim_models.gensim_transform import make_models

if __name__=='__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    names={'dictionary':'deep2.dict','corpus':'corpus2.mm','tfidf':'model2.tfidf'
           ,'lsi_model':'model2.lsi','lsi_index':'index2.lsi','lda_model':'model2.lda','lda_index':'index2.lda'}

    def initialize():

        corpus=gensim_preprocess.CorpusMaker(fromDB=True) #('/home/kel/deep.csv')

        corpus.dictionary.save(names['dictionary'])
        MmCorpus.serialize(fname=names['corpus'],corpus=corpus)

        tfidf = models.TfidfModel(corpus=corpus, dictionary=corpus.dictionary)
        tfidf.save(names['tfidf'])
        corpus_tfidf = tfidf[corpus]


        lsi = models.LsiModel(corpus_tfidf)

        corpus = gensim.corpora.MmCorpus(names['corpus'])
        dict=gensim.corpora.Dictionary.load((names['dictionary']))

        lsi.save(names['lsi_model'])
        index_lsi = similarities.MatrixSimilarity(lsi[corpus])
        index_lsi.save(names['lsi_index'])


        lda = models.LdaModel(corpus_tfidf)

        index_lda = similarities.MatrixSimilarity(lda[corpus])
        index_lda.save(names['lda_index'])

    def make_models():
        dictionary = gensim.corpora.Dictionary.load(names['dictionary'])
        corpus = gensim.corpora.MmCorpus(names['corpus'])

        tfidf = models.TfidfModel.load(names['tfidf'])

        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary)

        corpus_lsi = lsi[corpus_tfidf]

        lsi.save(names['lsi_model'])

        index = similarities.MatrixSimilarity(lsi[corpus])
        # index=similarities.Similarity(output_prefix='./',corpus=lsi[corpus])
        index.save(names['lsi_index'])


    #initialize()
    make_models()

