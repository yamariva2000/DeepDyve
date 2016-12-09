from gensim import corpora
from gensim.models import doc2vec,Doc2Vec
import gensim
import collections
documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]



model = gensim.models.doc2vec.Doc2Vec(size=20 ,min_count=2, iter=10)


docs=[]





for i,d in enumerate(documents):
    tdoc=doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(d),tags=[i])
    docs.append(tdoc)




model.build_vocab(docs)

model.train(docs)


# Let's count how each document ranks with respect to the training corpusranks= []
second_ranks = []
for doc_id in range(len(docs)):
    inferred_vector = model.infer_vector(docs[doc_id].words)
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    print sims
    rank = [docid for docid, sim in sims].index(doc_id)

    second_ranks.append(sims[1])


# In[12]:


#
# x=model.infer_vector(docs[0])
#
# print x
#
# print model.docvecs[0]





#print model.docvecs.most_similar([x],topn=9)


