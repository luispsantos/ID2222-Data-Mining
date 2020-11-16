import itertools
import time
from collections import defaultdict

class Apriori:

    def __init__(self, data='T10I4D100K.dat', s=10000):
        self.data= data
        self.s=s
        self.C_k=defaultdict(int)
        self.L={}

    def first_pass(self, item):
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

    # enkel model tills vidare
    def subset(self, Ck, t,k):
        return [c for c in itertools.combinations(t, k) if c in Ck]

    def algorithm(self, print_=True):
        basket_list=[]
        with open(self.data, 'r') as f:
            for basket in f:
                basket_list.append([self.first_pass(int(item)) for item in basket.split()])
        self.L[1]={(item,):self.C_k[item] for item in sorted(self.C_k) if self.C_k[item] >= self.s}
        k=1
        while len(self.L[k])!=0:
            t_k=time.time()
            k+=1
            C_k=self.apriori_gen(self.L[k-1],k)
            for t in basket_list:
                C_t=self.subset(C_k,t,k)
                for c in C_t:
                    C_k[c]+=1
            self.L[k]={item:C_k[item] for item in C_k if C_k[item]>=self.s}
            if print_:
                print(k,"- itemset time",time.time()-t_k,"L_"+str(k)+"  is ",len(self.L[k]))
        # the last one is empty should we remove it? ->  self.L.pop(len(self.L))
        return self.L

class FindAR:

    def find_association_rules(self,L, c=0.5, print_=True, option=1):
        if option==1:
            rules=[[subset,k1]for k in range(2, len(L)) for key in L[k].keys() for subset in
                   itertools.combinations(key,k-1) for k1 in key if k1 not in subset if c<L[k][key]/L[k-1][subset]]

        elif option==2:
            rules=[[subset,{k1 for k1 in key if k1 not in subset}] for k in range(2, len(L)) for k_ in range(1,k)
                   for key in L[k].keys() for subset in itertools.combinations(key,k_) if c<L[k][key]/L[k_][subset]]

        if print_:
            for rule in rules:
                print(rule[0],"->",rule[1])
        return rules

t=time.time()
L_k=Apriori(data='T10I4D100K.dat', s=1000).algorithm()
print(time.time()-t )

t=time.time()
FindAR().find_association_rules(L_k, option=2)
print(time.time()-t)
# original for find assosiation rule
# without last pop
# for k in range(2, len(L)):
#     for key in L[k].keys():
#         subsets= [subset for subset in itertools.combinations(key,k-1)]
#         for subset in subsets:
#             if c<L[k][key]/L[k-1][subset]:
#                 print(subset,"->",[k1 for k1 in key if k1 not in subset][0],": ",k,L[k][key]/L[k-1][subset])