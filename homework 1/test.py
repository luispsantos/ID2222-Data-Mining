from dataset_reader import read_webhose_dataset
from hw_classes import Shingling, CompareSets, MinHashing, CompareSignatures

# read the covid dataset
docs = read_webhose_dataset('covid-discussions.zip', 100)

shingling = Shingling()
compare_sets = CompareSets()
min_hashing = MinHashing(500)
compare_signatures = CompareSignatures()

# testing for documents 1 and 3
doc_1 = shingling.create_unique_shingles(docs[0])
doc_3 = shingling.create_unique_shingles(docs[2])

print(compare_sets.jaccard_similarity(doc_1, doc_3))

un_hashed_doc_1 = shingling.create_un_hashed_shingles(docs[0])
un_hashed_doc_3 = shingling.create_un_hashed_shingles(docs[2])

print(compare_sets.jaccard_similarity(un_hashed_doc_1, un_hashed_doc_3))

doc_idxs = [0, 2]
doc_list = [docs[doc_idx] for doc_idx in doc_idxs]
doc_shingles, n_shingles = shingling.create_document_shingles(doc_list)

signature = min_hashing.compute_signature(doc_shingles, n_shingles)
print(compare_signatures.signature_similarity(signature, 0, 1))