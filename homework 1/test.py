from dataset_reader import read_webhose_dataset
from preprocessor import TextPreprocessor
from hw_classes import Shingling, CompareSets, MinHashing, CompareSignatures, LSH

# read the covid dataset
docs = read_webhose_dataset('covid-blog-posts.zip', 100)
#docs = read_webhose_dataset('covid-discussions.zip', 100)

preprocessor = TextPreprocessor()
shingling = Shingling(10)
min_hashing = MinHashing(500)
lsh = LSH(100)

# testing for documents 1 and 3
doc_1 = shingling.create_unique_shingles(docs[0])
doc_3 = shingling.create_unique_shingles(docs[2])

print(CompareSets.jaccard_similarity(doc_1, doc_3))

un_hashed_doc_1 = shingling.create_un_hashed_shingles(docs[0])
un_hashed_doc_3 = shingling.create_un_hashed_shingles(docs[2])

print(CompareSets.jaccard_similarity(un_hashed_doc_1, un_hashed_doc_3))

# testing for a collection of 10 documents
doc_idxs = [0, 1, 3, 4, 6, 8, 13, 25, 39, 73]
doc_list = [docs[idx] for idx in doc_idxs]

clean_docs = preprocessor.preprocess_documents(doc_list)
char_matrix = shingling.create_characteristic_matrix(clean_docs)

signature_hash = min_hashing.compute_signature_hash(char_matrix)
print('signature hashing:', CompareSignatures.signature_similarity(signature_hash, 0, 1))

signature_perm = min_hashing.compute_signature_perm(char_matrix)
print('signature permutation:', CompareSignatures.signature_similarity(signature_perm, 0, 1))

similar_documents = lsh.find_similar(signature_hash)
print('similar documents:', similar_documents)
