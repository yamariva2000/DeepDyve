from gensim import corpora, models, similarities


def make_models():
    dictionary = corpora.Dictionary.load('deep.dict')
    corpus = corpora.MmCorpus('corpus.mm')

    tfidf = models.TfidfModel(corpus=corpus,dictionary=dictionary)

    corpus_tfidf=tfidf[corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary)

    corpus_lsi=lsi[corpus_tfidf]



    tfidf.save('model.tfidf')
    lsi.save('model.lsi')
    #corpus_tfidf.save('model.corpus_tfidf')

