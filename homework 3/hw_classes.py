import random
import itertools
from collections import defaultdict
from dataset_reader import read_snap_dataset


class SubGraph:
    """Sub-graph G containing only the edges in a sample S implemented as an adjacency list"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.adj_list = defaultdict(set)
        self.edge_set = set()

    def add_edge(self, u, v):
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)
        self.edge_set.add((u, v))

        if self.verbose:
            print(f'Adding edge ({u}, {v})')
            print(f'N({u}) = {self.adj_list[u]}, N({v}) = {self.adj_list[v]}')

    def remove_edge(self, u, v):
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)
        self.edge_set.remove((u, v))

        if self.verbose:
            print(f'Removing edge ({u}, {v})')
            print(f'N({u}) = {self.adj_list[u]}, N({v}) = {self.adj_list[v]}')

        # remove the nodes from the adjacency list if their degree is 0
        if not self.adj_list[u]:
            del self.adj_list[u]
        if not self.adj_list[v]:
            del self.adj_list[v]

    def has_node(self, u):
        return u in self.adj_list

    def has_edge(self, u, v):
        return (u, v) in self.edge_set

    def get_nodes(self):
        return list(self.adj_list)

    def get_edges(self):
        return list(self.edge_set)

    def get_neighbors(self, u):
        return self.adj_list.get(u)


class TriestBase:
    """Implementation of the Triest-Base Algorithm"""

    def __init__(self, M, verbose=False):
        self.M = M
        self.verbose = verbose
        self.subgraph = SubGraph(verbose)
        self.global_counter = 0
        self.local_counters = defaultdict(int)

    def sample_edge(self, t):
        # base case of reservoir sampling - always inserts the new edge
        if t <= self.M:
            return True

        # simulates flipping a biased coin with the heads probability M/t
        elif random.random() < self.M / t:
            # obtain a random edge from our graph
            edge_list = self.subgraph.get_edges()
            w, z = random.choice(edge_list)

            # remove the sampled edge from subgraph
            self.subgraph.remove_edge(w, z)
            self.update_counters('-', w, z)
            return True

        return False

    def update_counters(self, operation, u, v):
        # make sure the subgraph contains both nodes the edge leads to
        if not self.subgraph.has_node(u) or not self.subgraph.has_node(v):
            return

        neighbors_u = self.subgraph.get_neighbors(u)
        neighbors_v = self.subgraph.get_neighbors(v)

        shared_neighbors = neighbors_u & neighbors_v
        incr_value = 1 if operation == '+' else -1
        #print(shared_neighbors, neighbors_u, neighbors_v, self.global_counter)

        # update the global/local counters of the shared neighborhood
        for c in shared_neighbors:
            self.global_counter += incr_value
            self.local_counters[c] += incr_value
            self.local_counters[u] += incr_value
            self.local_counters[v] += incr_value

        if operation == '-':
            # delete the local counters containing a value of 0
            for c in itertools.chain(shared_neighbors, (u, v)):
                if not self.local_counters[c]:
                    del self.local_counters[c]

    def compute_eta(self, t):
        return max(1, t*(t-1)*(t-2) / (self.M*(self.M-1)*(self.M-2)))

    def algorithm(self, dataset_file):
        edge_stream = read_snap_dataset(dataset_file)
        t = 0

        for u, v in edge_stream:
            if u == v:
                continue
            elif u > v:
                v, u = u, v
            if self.subgraph.has_edge(u, v):
                continue

            t += 1
            if self.sample_edge(t):
                self.subgraph.add_edge(u, v)
                self.update_counters('+', u, v)

        eta_t = self.compute_eta(t)
        global_triangles = int(eta_t * self.global_counter)
        if self.verbose:
            print(f'Global triangles estimate: {global_triangles}')

        return global_triangles


class TriestImpr:
    """Implementation of the Triest-Impr Algorithm"""

    def __init__(self, M, verbose=False):
        self.M = M
        self.verbose = verbose
        self.subgraph = SubGraph(verbose)
        self.global_counter = 0
        self.local_counters = defaultdict(int)

    def sample_edge(self, t):
        # base case of reservoir sampling - always inserts the new edge
        if t <= self.M:
            return True

        # simulates flipping a biased coin with the heads probability M/t
        elif random.random() < self.M / t:
            # obtain a random edge from our graph
            edge_list = self.subgraph.get_edges()
            w, z = random.choice(edge_list)

            # remove the sampled edge from subgraph
            self.subgraph.remove_edge(w, z)
            return True

        return False

    def update_counters(self, t, u, v):
        # make sure the subgraph contains both nodes the edge leads to
        if not self.subgraph.has_node(u) or not self.subgraph.has_node(v):
            return

        neighbors_u = self.subgraph.get_neighbors(u)
        neighbors_v = self.subgraph.get_neighbors(v)

        shared_neighbors = neighbors_u & neighbors_v
        incr_value = self.compute_eta(t)

        # update the global/local counters of the shared neighborhood
        for c in shared_neighbors:
            self.global_counter += incr_value
            self.local_counters[c] += incr_value
            self.local_counters[u] += incr_value
            self.local_counters[v] += incr_value

    def compute_eta(self, t):
        return max(1, (t-1)*(t-2) / (self.M*(self.M-1)))

    def algorithm(self, dataset_file):
        edge_stream = read_snap_dataset(dataset_file)
        t = 0

        for u, v in edge_stream:
            if u == v:
                continue
            elif u > v:
                v, u = u, v
            if self.subgraph.has_edge(u, v):
                continue

            t += 1
            self.update_counters(t, u, v)
            if self.sample_edge(t):
                self.subgraph.add_edge(u, v)

        global_triangles = int(self.global_counter)
        if self.verbose:
            print(f'Global triangles estimate: {global_triangles}')

        return global_triangles
