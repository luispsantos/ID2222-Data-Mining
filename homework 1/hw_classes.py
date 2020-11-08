import itertools
import operator
import numpy as np
import string
import sympy
import unicodedata
from scipy.sparse import csr_matrix


class TextPreprocessor:
    def __init__(self, lowercase=True, remove_punctuation=True, remove_accents=True, normalize_whitespace=True):
        self.lowercase = lowercase
        self.remove_accents = remove_accents
        self.remove_punctuation = remove_punctuation
        self.normalize_whitespace = normalize_whitespace

    def strip_accents(self, doc):
        doc_nfkd = unicodedata.normalize('NFKD', doc)
        doc_ascii = doc_nfkd.encode('ASCII', 'ignore').decode('ascii')

        return doc_ascii

    def preprocess_document(self, doc):
        if self.lowercase:
            doc = doc.lower()

        if self.remove_accents:
            doc = self.strip_accents(doc)

        if self.remove_punctuation:
            doc = ''.join(char for char in doc if char not in string.punctuation)

        if self.normalize_whitespace:
            doc = ' '.join(doc.split())

        return doc


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
        # obtain a mapping of {shingle -> shingle index} over all shingles
        unique_shingles = set(shingle for shingles in doc_shingles for shingle in shingles)
        shingle_idxs = {shingle: idx for idx, shingle in enumerate(sorted(unique_shingles))}
        return doc_shingles, shingle_idxs

    def create_characteristic_matrix(self, doc_list):
        doc_shingles, shingle_idxs = self.create_document_shingles(doc_list)
        n_docs, n_shingles = len(doc_shingles), len(shingle_idxs)

        l = [(shingle_idxs[shingle], doc_id, 1) for doc_id, shingles in enumerate(doc_shingles) for shingle in shingles]
        shingle_indices, doc_indices, data = zip(*l)

        char_matrix = csr_matrix((data, (shingle_indices, doc_indices)), shape=(n_shingles, n_docs), dtype=np.bool_)
        return char_matrix


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

    def compute_signature_perm(self, doc_shingles, n_shingles):
        n_signature, n_docs = self.n_signature, len(doc_shingles)

        unique_shingles = set(shingle for shingles in doc_shingles for shingle in shingles)
        shingle_idxs = {shingle: idx for idx, shingle in enumerate(sorted(unique_shingles))}

        l = [(shingle_idxs[shingle], doc_id) for doc_id, doc in enumerate(doc_shingles) for shingle in doc]
        a, b = zip(*l)

        M = csr_matrix(([1]*len(a), (a, b)), shape=(n_shingles, n_docs), dtype=np.bool_)
        signature = np.zeros((n_signature, n_docs), dtype=np.int32)

        for i in range(n_signature):
            rand_idxs = np.random.permutation(n_shingles)
            M_permuted = M[rand_idxs, :]

            signature[i, :] = np.argmax(M_permuted, axis=0)

        return signature


class CompareSignatures:

    def signature_similarity(self, signature, doc_1, doc_2):
        # the fraction of elements with equal minhash signatures
        return np.mean(signature[:, doc_1] == signature[:, doc_2])

# class LSH
