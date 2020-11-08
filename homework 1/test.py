from dataset_reader import read_webhose_dataset
from preprocessor import TextPreprocessor
from hw_classes import Shingling, CompareSets, MinHashing, CompareSignatures

# read the covid dataset
docs = read_webhose_dataset('covid-blog-posts.zip', 100)
#docs = read_webhose_dataset('covid-discussions.zip', 100)

preprocessor = TextPreprocessor()

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

doc_idxs = [0, 1, 3, 4, 5]
doc_list = [docs[idx] for idx in doc_idxs]

clean_docs = preprocessor.preprocess_documents(doc_list)
char_matrix = shingling.create_characteristic_matrix(clean_docs)

signature_hash = min_hashing.compute_signature_hash(char_matrix)
print('signature hashing:', compare_signatures.signature_similarity(signature_hash, 0, 1))

signature_perm = min_hashing.compute_signature_perm(char_matrix)
print('signature permutation:', compare_signatures.signature_similarity(signature_perm, 0, 1))
