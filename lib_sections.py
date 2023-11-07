import networkx as nx

# Function taking json as input, return networkx graph
def dict_to_graph(library_dict: dict, sections_attrs: dict, connections: dict):
    '''
    Convert dictionaries into a networkx Graph representing the library's structure and connections.

    Args:
    - library_dict (dict): JSON data representing the library's layout and sections
    - sections_attrs (dict): Attributes and properties of the sections in the library
    - connections (dict): Information about gates, levels, and their connections
    
    Frontend request must be in format of static/lib_sections.json\\
    sections_attrs follow the format of static/sections_attrs.json\\
    connections follow the format of static/connections.json

    Returns:
    - nx.Graph: Graph representation of the library
    '''
    # Create an empty graph with attributes from library_dict
    G = nx.Graph(submission_name=library_dict['submission_name'])

    # Add nodes and attributes to the graph based on the input dictionaries
    for levels_dict in library_dict['levels']:
        level_id = f"{levels_dict['level']}"
        G.add_node(level_id)
        for sections_dict in levels_dict['sections']:
            section_id = f"{levels_dict['level']}-{sections_dict['seat_type']}"
            # Add nodes with attributes from sections_attrs and sections_dict
            G.add_node(
                section_id, 
                **sections_dict, 
                **sections_attrs[sections_dict['seat_type']], 
                level=levels_dict['level'], 
                empty_seats=sections_dict['capacity']
            )
            G.add_edge(level_id, section_id)  # Connect level to section

    # Add edges for gates and connections       
    for connection in connections['gates']:
        G.add_edge(connection['gate_id'], connection['connected_to'])
    for connection in connections['levels']:
        G.add_edge(connection['level_id'], connection['connected_to'])
    
    # Return the networkx Graph representing the library
    return G
