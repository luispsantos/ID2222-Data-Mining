import itertools
import operator
import numpy as np
import sympy


class Shingling:

    def __init__(self, k_shingles=10):
        self.k_shingles = k_shingles

    def create_unique_shingles(self, doc):
        unique_shingles = sorted(set([self.hash_shingles(doc[i:(i + self.k_shingles)]) for i in range(len(doc) - self.k_shingles)]))
        # print(unique_shingles)
        return unique_shingles

    def hash_shingles(self, shingle):
        hashed_shingle = sum([pow(10, char_idx) * ord(character) for char_idx, character in enumerate(shingle)]) % (2**32)
        return hashed_shingle

    # not part of the homework this is just to compare to un hashed similarities
    def create_un_hashed_shingles(self, doc):
        un_hashed_shingle = sorted(set([doc[i:(i + self.k_shingles)] for i in range(len(doc) - self.k_shingles)]))
        # print(un_hashed_shingle)
        return un_hashed_shingle

    def create_document_shingles(self, doc_list):
        doc_shingles = [self.create_unique_shingles(doc) for doc in doc_list]
        n_shingles = len(set(shingle for shingles in doc_shingles for shingle in shingles))
        return doc_shingles, n_shingles


class CompareSets:

    # intersection / union
    def jaccard_similarity(self, set_1, set_2):
        set_1, set_2 = set(set_1), set(set_2)
        similarity = len(set_1.intersection(set_2)) / len(set_1.union(set_2))
        return similarity


class MinHashing:

    def __init__(self, n_signature):
        self.n_signature = n_signature

    def compute_signature(self, doc_shingles, n_shingles):
        n_signature, n_docs = self.n_signature, len(doc_shingles)

        # initialize the signature matrix with +infinity
        hashes = np.zeros(n_signature, dtype=np.int32)
        signature = np.full((n_signature, n_docs), np.inf)

        # choose n_signature random parameters for a and b (both numbers are bounded by p)
        p = sympy.nextprime(n_shingles)
        a = 2 * np.random.randint(0, p//2, n_signature) + 1  # a is always an odd number
        b = np.random.randint(0, p, n_signature)

        # sort the document-shingle pairs and order by shingle
        sorted_shingles = sorted((shingle, doc_id) for doc_id, doc in enumerate(doc_shingles) for shingle in doc)

        for row_idx, (shingle, doc_ids) in enumerate(itertools.groupby(sorted_shingles, key=operator.itemgetter(0))):
            # compute n_signature independent hash functions
            for i in range(n_signature):
                hashes[i] = self.compute_universal_hash(row_idx, a[i], b[i], p, n_shingles)

            #print(row_idx, hashes)
            for _, doc_id in doc_ids:
                for i in range(n_signature):
                    if hashes[i] < signature[i, doc_id]:
                        #print(f'({i}, {doc_id}): {signature[i, doc_id]} -> {hashes[i]}')
                        signature[i, doc_id] = hashes[i]

        return signature

    def compute_universal_hash(self, x, a, b, p, m):
        # for more information check: https://en.wikipedia.org/wiki/Universal_hashing#Hashing_integers
        return ((a*x + b) % p) % m

class CompareSignatures:

    def signature_similarity(self, signature, doc_1, doc_2):
        # the fraction of elements with equal minhash signatures
        return np.mean(signature[:, doc_1] == signature[:, doc_2])

# class LSH
