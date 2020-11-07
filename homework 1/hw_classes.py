from functools import reduce
import numpy as np

class Shingling:

    def __init__(self, k_shingles=10):
        self.k_shingles=k_shingles

    def create_unique_shingles(self, doc):
        unique_shingles=sorted(set([self.hash_shingles(doc[i:(i + self.k_shingles)]) for i in range(len(doc) - self.k_shingles)]))
        print(unique_shingles)
        return unique_shingles

    def hash_shingles(self, shingle):
        hashed_shingle = sum([pow(10,i)*ord(character) for i, character in enumerate(shingle)])%(2**32)
        return hashed_shingle

    # not part of the homework this is just to compare to un hashed similarities
    def create_un_hashed_shingles(self, doc):
        un_hashed_shingle=sorted(set([doc[i:(i + self.k_shingles)] for i in range(len(doc) - self.k_shingles)]))
        print(un_hashed_shingle)
        return un_hashed_shingle


class CompareSets:

    # intersection / union
    def jaccard_similarity(self,set_1,set_2):
        set_1,set_2=set(set_1),set(set_2)
        similarity= len(set_1.intersection(set_2))/ len(set_1.union(set_2))
        return similarity



class MinHashing:

    def __init__(self, n_rows, n_doc):
        self.signature=np.full((n_rows,n_doc), np.inf)

    def compute_signature(self, doc_list):
        shingling=Shingling()
        doc_shingles=[shingling.create_unique_shingles(doc) for doc in doc_list]
        doc_shingles=sorted([(doc_id, shingle) for doc_id, doc in enumerate(doc_shingles) for shingle in doc], key=lambda  x: x[1])

    #def compute_hash(self, row_idx, a, b):

#class CompareSignatures()

#class LSH()

