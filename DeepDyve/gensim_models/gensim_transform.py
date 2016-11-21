from gensim import corpora, models, similarities


def make_models():
    dictionary = corpora.Dictionary.load('deep.dict')
    corpus = corpora.MmCorpus('corpus.mm')

    tfidf = models.TfidfModel(corpus=corpus,dictionary=dictionary)

    corpus_tfidf=tfidf[corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary)

    corpus_lsi=lsi[corpus_tfidf]
raw_input()


    tfidf.save('model.tfidf')
    lsi.save('model.lsi')

    index = similarities.MatrixSimilarity(lsi[corpus])
    # index=similarities.Similarity(output_prefix='./',corpus=lsi[corpus])
    index.save('index.lsi')


    #corpus_tfidf.save('model.corpus_tfidf')

