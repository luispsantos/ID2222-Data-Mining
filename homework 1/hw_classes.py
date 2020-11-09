import itertools
import numpy as np
import sympy
from scipy import sparse
from collections import defaultdict


class Shingling:

    def __init__(self, k_shingles=10):
        self.k_shingles = k_shingles

    def create_unique_shingles(self, doc):
        unique_shingles = sorted(set([self.hash_shingles(doc[i:(i + self.k_shingles)]) for i in range(len(doc) - self.k_shingles)]))
        # print(unique_shingles)
        return unique_shingles

    def hash_shingles(self, shingle):
        hashed_shingle = sum([pow(100, char_idx) * ord(character) for char_idx, character in enumerate(shingle)]) % (2**32)
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

        vals = [(shingle_idxs[shingle], doc_id, 1) for doc_id, shingles in enumerate(doc_shingles) for shingle in shingles]
        shingle_indices, doc_indices, data = zip(*vals)

        char_matrix = sparse.csr_matrix((data, (shingle_indices, doc_indices)), shape=(n_shingles, n_docs), dtype=np.bool_)
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

    def compute_signature_hash(self, char_matrix):
        n_signature, (n_shingles, n_docs) = self.n_signature, char_matrix.shape

        # initialize the signature matrix with +infinity
        signature = np.full((n_signature, n_docs), np.inf)

        # choose n_signature random parameters for a and b (both numbers are bounded by p)
        p = sympy.nextprime(n_shingles)
        a = 2 * np.random.randint(0, p//2, n_signature) + 1  # a is always an odd number
        b = np.random.randint(0, p, n_signature)

        # iterate over the rows (each row representing a shingle)
        for row_idx, doc_ids in enumerate(char_matrix.tolil().rows):
            # compute n_signature independent hash functions
            hashes = self.compute_universal_hash(row_idx, a, b, p, n_shingles)
            #print(row_idx, hashes)

            # iterate over the documents which contain that shingle
            for doc_id in doc_ids:
                signature[:, doc_id] = np.where(hashes < signature[:, doc_id], hashes, signature[:, doc_id])

        return signature

    def compute_universal_hash(self, x, a, b, p, m):
        # for more information check: https://en.wikipedia.org/wiki/Universal_hashing#Hashing_integers
        # for choice of parameters check also: https://stackoverflow.com/a/25104050/9244026
        return ((a*x + b) % p) % m

    def compute_signature_perm(self, char_matrix):
        n_signature, (n_shingles, n_docs) = self.n_signature, char_matrix.shape

        # initialize the signature matrix with zeros
        signature = np.zeros((n_signature, n_docs), dtype=np.int32)

        for idx in range(n_signature):
            # permute the rows of the characteristic matrix
            rand_idxs = np.random.permutation(n_shingles)
            char_matrix_perm = char_matrix[rand_idxs, :]

            # the minhash is the row-wise position of the first one
            signature[idx, :] = np.argmax(char_matrix_perm, axis=0)

        return signature


class CompareSignatures:

    def signature_similarity(self, signature, doc_1, doc_2):
        # the fraction of elements with equal minhash signatures
        return np.mean(signature[:, doc_1] == signature[:, doc_2])


class LSH:

    def __init__(self, n_bands=10, sim_threshold=0.75):
        self.n_bands = n_bands
        self.sim_threshold = sim_threshold

    def find_candidates(self, signature):
        n_bands, (n_signature, n_docs) = self.n_bands, signature.shape

        band_rows = n_signature // n_bands
        candidate_pairs = set()
        column_buckets = defaultdict(list)

        for band_idx in range(n_bands):
            # obtain the chunk of rows which correspond to a band
            band = signature[band_idx * band_rows:(band_idx+1) * band_rows]

            # iterate over the columns which belong to this band
            for doc_id, column in enumerate(band.T):
                # store all documents in this band with identical hashes
                # we must convert the vector to a tuple so it's hashable
                column_buckets[tuple(column)].append(doc_id)

            for doc_ids in column_buckets.values():
                pairwise_combinations = itertools.combinations(doc_ids, 2)
                candidate_pairs.update(pairwise_combinations)

            # clear the buckets - each band uses an independent hash table
            column_buckets.clear()

        return candidate_pairs
