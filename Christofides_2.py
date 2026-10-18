#   Title: Christofides.py
#
#   Description: graph data structure implementation and christophides TSP algorithm
#                
#                Sources: https://alon.kr/posts/christofides
#                         https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
#   
#   Author: Monem Moheq
#
#   Date: Oct 17


import pandas as pd
import numpy as np
import networkx as nx
import sys    
        
def main():

    dist_csv = pd.read_csv("Pairwise Distances.csv")
    distances = dist_csv.iloc[:,1:]
    distances.index = dist_csv.iloc[:,0].values

    G = nx.Graph()
    for v_1 in distances.index:
        for v_2 in distances.index:
            G.add_edge(v_1, v_2, weight = distances.loc[v_1][v_2])
    G.remove_edges_from(nx.selfloop_edges(G))

    # print(f"Nodes: {G.nodes}") 
    # print(f"Edges: {G.edges}") 

    # christophides
    # 1. Get minimum spanning tree
    T = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
    U = []
    for v in T.degree:
        if v[1] % 2 == 1:
            U.append(v[0])
    
    # Get edges with odd degree in T
    subgraph_U = G.subgraph(U)

    # 3. finding Minimum Weight Perfect Matching for you U
    J = nx.min_weight_matching(subgraph_U, weight='weight')

    # 4. Merge MPM and MST
    T_prime = nx.MultiGraph()
    T_prime.add_nodes_from(T.nodes())
    T_prime.add_edges_from(T.edges(data=True))

    for u, v in J:
        edge_weight = G[u][v]['weight'] 
        T_prime.add_edge(u, v, weight=edge_weight)
    #print(J)

    # 5. find eurerian circuit
    eulerian_edges = nx.eulerian_circuit(T_prime)

    C = []
    for e in eulerian_edges:
        C.append(e[0])
    
    # Shortest cycle of n edges
    C_prime = []
    visited = set()

    for v in C:
        if v not in visited:
            C_prime.append(v)
            visited.add(v)

    if C_prime:
        C_prime.append(C_prime[0])

    print(C_prime)

if __name__ == "__main__":
    sys.exit(main())
