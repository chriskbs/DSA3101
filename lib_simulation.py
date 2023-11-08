from lib_model import LibModel
from lib_sections import create_default_graph
import json


def run_simulation(df, path_to_capacities, exam_period = False):
    lib_graph = create_default_graph(path_to_capacities)
    model = LibModel(df, lib_graph, exam_period)
    model.run()
    results = model.datacollector.get_table_dataframe("SectionsData")
    results['utilization_rate'] = 1-results['empty_seats']/results['capacity']
    return results