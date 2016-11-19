import spacy

import csv

'''['__bytes__', '__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__new__', '__pyx_vtable__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '_py_tokens', '_realloc', '_vector', '_vector_norm', 'count_by', 'ents', 'from_array', 'from_bytes', 'has_vector', 'is_parsed', 'is_tagged', 'mem', 'merge', 'noun_chunks', 'noun_chunks_iterator', 'read_bytes', 'sentiment', 'sents', 'similarity', 'string', 'tensor', 'text', 'text_with_ws', 'to_array', 'to_bytes', 'user_data', 'user_hooks', 'user_span_hooks', 'user_token_hooks', 'vector', 'vector_norm', 'vocab']'''



nlp=spacy.load('en')
nlp.pipeline=[nlp.tagger]


class IterCorpus(object):
    def __iter__(self):
        for line in open('../deep.csv'):
            yield unicode(line)

iterdata=IterCorpus()


pipe=nlp.pipe(iterdata, batch_size=50, n_threads=4)
#
#
# for i, doc in enumerate(nlp.pipe(iterdata, batch_size=50, n_threads=4)):
#
#     print doc
#
#     if i == 100:
#         break

for i in pipe:

    print i[0]
    print next(i.sents)


    assert False