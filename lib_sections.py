import networkx as nx

# Function taking json as input, return networkx graph
def dict_to_graph(library_dict: dict, sections_attrs: dict, connections: dict):
    """
    Frontend request must be in format of static/lib_sections.json\\
    sections_attrs follow the format of static/sections_attrs.json\\
    connections follow the format of static/connections.json
    """
    G = nx.Graph(submission_name=library_dict['submission_name'])
    for levels_dict in library_dict['levels']:
        level_id = f"{levels_dict['level']}"
        G.add_node(level_id)
        for sections_dict in levels_dict['sections']:
            section_id = f"{levels_dict['level']}-{sections_dict['seat_type']}"
            G.add_node(section_id, **sections_dict, **sections_attrs[sections_dict['seat_type']], level=levels_dict['level'])
            G.add_edge(level_id, section_id)
    for connection in connections['gates']:
        G.add_edge(connection['gate_id'], connection['connected_to'])
    for connection in connections['levels']:
        G.add_edge(connection['level_id'], connection['connected_to'])
    return G