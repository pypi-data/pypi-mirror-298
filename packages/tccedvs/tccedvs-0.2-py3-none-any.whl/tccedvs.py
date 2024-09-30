"""2 Club Cluster Edge Deletion with Vertex Splitting"""

__version__ = "0.2"

import networkx as nx
import time

def has_diameter_at_most_2(G, nodes):
    '''function that checks if a subgraph has a diameter of at most 2'''
    subgraph = G.subgraph(nodes)
    if not nx.is_connected(subgraph):
        return False
    try:
        return max(nx.eccentricity(subgraph).values()) <= 2
    except nx.NetworkXError:
        return False

def try_split_vertex(G, v):
    '''function that splits a vertex with degree 4  or more if the split results in a 2 club'''
    neighbors = list(G.neighbors(v))
    if len(neighbors) < 4:
        return False, None

    new_v = max(G.nodes()) + 1
    G_copy = G.copy()
    G_copy.add_node(new_v)

    split_point = len(neighbors) // 2
    for neighbor in neighbors[:split_point]:
        G_copy.remove_edge(v, neighbor)
        G_copy.add_edge(new_v, neighbor)

    cluster1 = {v} | set(G_copy.neighbors(v))
    cluster2 = {new_v} | set(G_copy.neighbors(new_v))

    if has_diameter_at_most_2(G_copy, cluster1) or has_diameter_at_most_2(G_copy, cluster2):
        return True, G_copy
    else:
        return False, None

def main():
    '''The main function reads the graph, computes the square clustering coefficient via networkx, and creates the initial clusters before attempting to split'''
    start_time = time.time()
    print("Please enter the path of the file containing your edge list: ")
    edge_list_file = input()
    G_nx = nx.read_edgelist(edge_list_file, nodetype=int, data=False)

    print("Original graph:", G_nx)

    initial_clusters = []
    unclustered_vertices = set(G_nx.nodes())
    for component in nx.connected_components(G_nx):
        if has_diameter_at_most_2(G_nx, component):
            initial_clusters.append(component)
            unclustered_vertices -= component

    print(f"Found {len(initial_clusters)} initial 2-Clubs")

    for v in list(G_nx.nodes()):
        split_successful, new_graph = try_split_vertex(G_nx, v)
        if split_successful:
            G_nx = new_graph

    print("Graph after splitting:", G_nx)

    # Calculate Square Clustering Coefficient
    square_cc = nx.square_clustering(G_nx)

    # Create clustering based on Square Clustering Coefficient
    sorted_vertices = sorted(square_cc.keys(), key=square_cc.get, reverse=True)

    clusters = {}
    while unclustered_vertices:
        for v in sorted_vertices:
            if v in unclustered_vertices:
                cluster = {v}
                candidates = set(nx.descendants_at_distance(G_nx, v, 1))
                candidates.update(nx.descendants_at_distance(G_nx, v, 2))

                for candidate in candidates:
                    if candidate in unclustered_vertices:
                        temp_cluster = cluster.union({candidate})
                        try:
                            if all(nx.shortest_path_length(G_nx.subgraph(temp_cluster), source=x, target=y) <= 2
                                   for x in temp_cluster for y in temp_cluster):
                                cluster.add(candidate)
                        except nx.NetworkXNoPath:
                            continue

                clusters[v] = cluster
                unclustered_vertices -= cluster
                break

    # Combine initial clusters with newly formed clusters
    final_clusters = initial_clusters + list(clusters.values())

    end_time = time.time()
    running_time = end_time - start_time

    print("\nFinal Clustering Results:")
    print(f"Number of clusters: {len(final_clusters)}")
    for i, cluster in enumerate(final_clusters, 1):
        print(f"Cluster {i}: {sorted(cluster)}")
    print(f"\nTotal running time: {running_time:.4f} seconds")

    with open("final_clustering_results.txt", "w") as f:
        f.write("Final Clustering Results:\n")
        f.write(f"Number of clusters: {len(final_clusters)}\n")
        for i, cluster in enumerate(final_clusters, 1):
            f.write(f"Cluster {i}: {sorted(cluster)}\n")
        f.write(f"\nTotal running time: {running_time:.4f} seconds")

    print(f"Final results have been written to final_clustering_results.txt")

if __name__ == "__main__":
    main()
