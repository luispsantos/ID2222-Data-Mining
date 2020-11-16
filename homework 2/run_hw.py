import time
import argparse
from hw_classes import Apriori, AssociationRules


parser = argparse.ArgumentParser(description='Find frequent itemsets and association rules for a given support/confidence')
parser.add_argument('-dataset-file', default='T10I4D100K.dat', help='name of a transactions dataset with baskets and items')
parser.add_argument('-s', default=1000, type=int, help='minimum support a itemset must have to be considered frequen')
parser.add_argument('-c', default=0.5, type=float, help='minimum confidence a rule must have to be generated')
parser.add_argument('-verbose', default=True, type=bool, help='decides if the results gets printed')


args = parser.parse_args()
print(args)

t=time.time()
apriori=Apriori(data=args.dataset_file, s=args.s)
L_k=apriori.algorithm(verbose=args.verbose)
if args.verbose:
    print("time for sub problem 1",time.time()-t )

t=time.time()
associationrules=AssociationRules()
rules=associationrules.find(L_k, c=args.c, verbose=args.verbose)
if args.verbose:
    print("time for sub problem 2",time.time()-t)


