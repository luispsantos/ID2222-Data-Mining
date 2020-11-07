from dataset_reader import *
from hw_classes import Shingling, CompareSets

# testing for documents 1 and 3
doc_1=Shingling().create_unique_shingles(docs[0])
doc_3=Shingling().create_unique_shingles(docs[2])

print(CompareSets().jaccard_similarity(doc_1, doc_3))

un_hashed_doc_1=Shingling().create_un_hashed_shingles(docs[0])
un_hashed_doc_3=Shingling().create_un_hashed_shingles(docs[2])

print(CompareSets().jaccard_similarity(un_hashed_doc_1, un_hashed_doc_3))

