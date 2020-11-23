import time
import argparse
from hw_classes import TriestBase, TriestImpr


parser = argparse.ArgumentParser(description='Find global/local triangle estimates in a streaming graph using TRIEST.')
parser.add_argument('-dataset-file', default='web-Stanford.txt.gz', help='path to a gzipped snap dataset')
parser.add_argument('-triest', default='impr', choices=['base', 'impr'], type=str, help='TRIEST algorithm')
parser.add_argument('-M', default=10000, type=int, help='size of the sample of edges used in reservoir sampling')
parser.add_argument('-verbose', default=False, action='store_true', help='decides if the results are printed')

args = parser.parse_args()
print(args)

if args.triest == 'base':
    triest = TriestBase(args.M, args.verbose)
else:
    triest = TriestImpr(args.M, args.verbose)

start_time = time.time()
global_triangles = triest.algorithm(args.dataset_file)

elapsed_time = time.time() - start_time
print(f'TRIEST-{args.triest.upper()} took {elapsed_time:.3f}s')
