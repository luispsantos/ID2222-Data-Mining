import itertools
import time
from collections import defaultdict

class Apriori:

    def __init__(self, data, s):
        self.data= data
        self.s=s
        self.C_k=defaultdict(int)
        self.L={}

    def first_pass(self, item):
        # add one to the count of this itemset(size 1)
        self.C_k[item]+=1
        return item

    # This function generates all the candidates C_k
    def apriori_gen(self, L, k):
        L_k=list(L.keys())

        # Create all candidates C_k

        # a bit faster
        #C_k={L_k[p][:k-1]+(L_k[q][k-2],):0 for p in range(len(L_k)-1) for q in range(p+1,len(L_k)) if L_k[p][:(k-2)]==L_k[q][:(k-2)]}

        # better looking code
        C_k={p[:(k-1)]+(q[k-2],):0 for p in L_k for q in L_k if p[:(k-2)]==q[:(k-2)] and q[k-2]>p[k-2] }

        # for all itemsets c if any of its subsets s is not in L_(k-1) remove c
        remove_list=[c for c in C_k for s in itertools.combinations(c, k-1) if s not in L]
        for i in remove_list:
            C_k.pop(i, None)
        return C_k

    # Simple version it add the
    def subset(self, Ck, t,k):
        return [c for c in itertools.combinations(t, k) if c in Ck]

    def algorithm(self, verbose):
        t_k = time.time()
        basket_list=[]
        with open(self.data, 'r') as f:
            for basket in f:
                basket_list.append([self.first_pass(int(item)) for item in basket.split()])
        # filter out itemsets that don't have at least support s
        self.L[1]={(item,):self.C_k[item] for item in sorted(self.C_k) if self.C_k[item] >= self.s}
        k=1
        while len(self.L[k])!=0:
            if verbose:
                print(k,"- itemset time",time.time()-t_k,"size of L_"+str(k)+"  is ",len(self.L[k]))
            t_k=time.time()
            k+=1
            # gets all candidates
            C_k=self.apriori_gen(self.L[k-1],k)
            for t in basket_list:
                # gets all candidates contained in t
                C_t=self.subset(C_k,t,k)
                # adds one to the count of all of these candidates
                for c in C_t:
                    C_k[c]+=1
            # filter out itemsets that don't have at least support s
            self.L[k]={item:C_k[item] for item in C_k if C_k[item]>=self.s}
        # the last one is empty that's why  we remove it!
        self.L.pop(len(self.L))
        return self.L

class AssociationRules:

    def find(self, L, c, verbose, option=1):
        if option==1:
            # add the associationrule X -> Y  to the list of rules if count(X+Y)/count(X) > c, size(Y)=1
            rules=[[subset,k1,L[k][key]/L[k-1][subset]]for k in range(2, len(L)+1) for key in L[k].keys() for subset in
                   itertools.combinations(key,k-1) for k1 in key if k1 not in subset if c<=L[k][key]/L[k-1][subset]]

        elif option==2:
            # add the associationrule X -> Y  to the list of rules if count(X+Y)/count(X) > c, size(Y)>=1
            rules=[[subset,{k1 for k1 in key if k1 not in subset}] for k in range(2, len(L)+1) for k_ in range(1,k)
                   for key in L[k].keys() for subset in itertools.combinations(key,k_) if c<=L[k][key]/L[k_][subset]]

        if verbose:
            for rule in rules:
                print(rule[0],"->",rule[1])
        return rules

