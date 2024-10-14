def add_hex_edges(graphs, graph_id, node_id, destination_node_ids):
    for id in destination_node_ids:
        graphs.add_graph_node_edge(graph_id, node_id, id, 'Connected')