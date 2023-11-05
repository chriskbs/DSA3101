import numpy as np
import pandas as pd
import mesa
import networkx as nx
from lib_agent import LibAgent

def compute_agents(model):
    return len(model.schedule.agents)

# def compute_empty_seats(model):
#   return {node: model.library_graph.nodes[node]['empty_seats'] for node in model.library_graph.nodes if 'empty_seats' in model.library_graph.nodes[node]}

class LibModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, df, library_graph):
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        entry_df = df.set_index('Datetime')
        entry_df = entry_df[entry_df['Direction']=='Entry']['Direction'].resample('10min',  label='left').count().reset_index()
        entry_df.columns = ['timestamp', 'entry_counts'] # how many entries every 10 mins

        self.schedule = mesa.time.RandomActivation(self)
        self._curr_step = 0
        self.entry_dist = entry_df.to_dict()['entry_counts']
        self.timestamps = entry_df.to_dict()['timestamp']
        self.total_steps = len(self.entry_dist) # total steps taken
        self.library_graph = library_graph

        self.datacollector = mesa.DataCollector(
            model_reporters={"num_agents": compute_agents},
            agent_reporters={"chosen_seat": "chosen_seat", "satisfaction": "satisfaction"},
            tables={"SectionsData":["timestamp", "section", "level", "capacity", "empty_seats"]}
        )

    def remove_agent_from_graph(self, agent_node):
        if self.library_graph.has_node(agent_node):
           self.library_graph.nodes[agent_node]['empty_seats'] +=1

    def find_optimal_seat(self, agent, distance_weight):
        path_costs = {}
        for node in self.library_graph.nodes:
          if 'empty_seats' in self.library_graph.nodes[node]:
            if self.library_graph.nodes[node]['empty_seats'] > 0:
                #don't need path anymore just need distance
                #path = nx.shortest_path(self.library_graph, source=agent.gate, target=node)
                path_length = nx.shortest_path_length(self.library_graph, source=agent.gate, target=node)
                
                # Agent will prefer those seats/sections with:
                # - high comfort, scenery, lighting, ease_find
                # - low crowd level (i.e. sections with low seat utilization rate)
                # The final seat score is calculated by taking weighted avg w.r.t the preferences
                seat_score = self.library_graph.nodes[node]['privacy'] * agent.privacy_pref + \
                    self.library_graph.nodes[node]['comfort'] * agent.comfort_pref + \
                    5*self.library_graph.nodes[node]['empty_seats']/self.library_graph.nodes[node]['capacity'] * agent.crowd_level_pref + \
                    self.library_graph.nodes[node]['scenery'] * agent.scenery_pref + \
                    self.library_graph.nodes[node]['lighting'] * agent.lighting_pref + \
                    self.library_graph.nodes[node]['ease_find'] * agent.ease_find_pref 
                
                # increase in path length means less desirability
                total_score = -distance_weight * path_length + seat_score

                if total_score >= agent.min_desirability_threshold:
                    path_costs[node] = total_score

        sorted_nodes = sorted(path_costs.items(), key=lambda item: item[1], reverse=True)
        
        if sorted_nodes:
            seat = sorted_nodes[0]
            return seat
        else:
            return None  # No available seat found

    def step(self):
        # Create agents, where number of agents follows Poisson distribution
        num_agents = self.entry_dist[self._curr_step]
        for i in range(np.random.poisson(num_agents)):
            agent = LibAgent(f'{self._curr_step}-{i}', self)
            # print(agent.unique_id, 'created!') # for debugging

            optimal_seat = self.find_optimal_seat(agent, 0.7)
            if optimal_seat is not None:
                agent.chosen_seat = optimal_seat[0]
                agent.satisfaction = optimal_seat[1]/agent.avg_pref
                self.library_graph.nodes[optimal_seat[0]]['empty_seats'] -= 1
                self.schedule.add(agent) # add to schedule
        
        self.datacollector.collect(self)
        # for table
        for node in self.library_graph.nodes:
            curr_node = self.library_graph.nodes[node]
            if 'empty_seats' in curr_node:
              curr_row = {"timestamp": self.timestamps[self._curr_step], "section": node, "level":curr_node['level'], "empty_seats": curr_node['empty_seats'], "capacity": curr_node['capacity']}
              self.datacollector.add_table_row("SectionsData", curr_row)

        self.schedule.step()
        self._curr_step += 1

    def run(self):
        for i in range(self.total_steps):
            self.step()