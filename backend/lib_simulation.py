from lib_model import LibModel
from lib_sections import create_default_graph
import json
import pandas as pd


def run_simulation(df, lib_sections, exam_period = False):
    lib_graph = create_default_graph(lib_sections)
    model = LibModel(df, lib_graph, exam_period)
    model.run()
    results = model.datacollector.get_table_dataframe("SectionsData")
    results['utilization_rate'] = 1-results['empty_seats']/results['capacity']

    
    sections_dict = dict()
    for nodes in lib_graph.nodes:
        node_data = lib_graph.nodes[nodes]
        if 'capacity' in node_data:
            sections_dict[nodes] = node_data
    sections_df = pd.DataFrame.from_dict(sections_dict, orient='index')

    return results, sections_df