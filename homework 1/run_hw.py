import argparse
from dataset_reader import read_webhose_dataset
from preprocessor import TextPreprocessor
from hw_classes import Shingling, CompareSets, MinHashing, CompareSignatures, LSH


parser = argparse.ArgumentParser(description='Find similar documents using minhashing and LSH techniques.')
parser.add_argument('-dataset-file', default='covid-blog-posts.zip', help='path to a webhose dataset')
parser.add_argument('-n-documents', default=100, type=int, help='number of documents to read from dataset')
parser.add_argument('-k-shingles', default=10, type=int, help='construct shingles of character length k')
parser.add_argument('-n-signature', default=500, type=int, help='build a minhash signature of length n')
parser.add_argument('-n-bands', default=100, type=int, help='number of bands for locality-sensitive hashing')
parser.add_argument('-sim-threshold', default=0.8, type=float, help='similarity threshold for retrieving documents')
parser.add_argument('-use-permutations', default=False, action='store_true', help='compute minhashing via permutations or hashing')

args = parser.parse_args()
print(args)

preprocessor = TextPreprocessor()
shingling = Shingling(args.k_shingles)
min_hashing = MinHashing(args.n_signature)
lsh = LSH(args.n_bands, args.sim_threshold)

docs = read_webhose_dataset(args.dataset_file, args.n_documents)
clean_docs = preprocessor.preprocess_documents(docs)
char_matrix = shingling.create_characteristic_matrix(clean_docs)

if args.use_permutations:
    signature = min_hashing.compute_signature_perm(char_matrix)
else:
    signature = min_hashing.compute_signature_hash(char_matrix)

similar_documents = lsh.find_similar(signature)
print('similar documents:', similar_documents)
