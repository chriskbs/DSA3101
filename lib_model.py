import numpy as np
import pandas as pd
import mesa
import networkx as nx
from lib_agent import LibAgent

def compute_agents(model):
    return len(model.schedule.agents)

class LibModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, entry_df, library_graph):
        self.schedule = mesa.time.RandomActivation(self)
        self._curr_step = 0
        self.entry_dist = entry_df.to_dict()['Direction']
        self.total_steps = len(self.entry_dist) # total steps taken
        self.library_graph = library_graph

        self.datacollector = mesa.DataCollector(
            model_reporters={"num_agents": compute_agents},
            agent_reporters={"chosen_seat": "chosen_seat", "satisfaction": "satisfaction"},
            collector= {"capacities": "capacity_data"}
        )

    def remove_agent_from_graph(self, agent_node):
        if self.library_graph.has_node(agent_node):
           self.library_graph.nodes[agent_node]['capacity'] +=1

    def find_optimal_seat(self, agent, distance_weight):
        path_costs = {}
        for node in self.library_graph.nodes:
          if 'capacity' in self.library_graph.nodes[node]:
            if self.library_graph.nodes[node]['capacity'] > 0:
                #don't need path anymore just need distance
                #path = nx.shortest_path(self.library_graph, source=agent.gate, target=node)
                path_length = nx.shortest_path_length(self.library_graph, source=agent.gate, target=node)
                
                #TODO settle the attributes for the seat score
                seat_score = self.library_graph.nodes[node]['privacy'] * agent.privacy_pref + \
                    self.library_graph.nodes[node]['comfort'] * agent.comfort_pref + \
                    self.library_graph.nodes[node]['occupied'] * agent.crowd_level_pref + \
                    self.library_graph.nodes[node]['scenery'] * agent.scenery_pref + \
                    self.library_graph.nodes[node]['lighting'] * agent.lighting_pref

                total_score = distance_weight * path_length + seat_score

                if total_score >= agent.min_desirability_threshold:
                    path_costs[node] = total_score

        sorted_nodes = sorted(path_costs.items(), key=lambda item: item[1])
        
        if sorted_nodes:
            seat = sorted_nodes[0]
            return seat
        else:
            return None  # No available seat found


    ''' the A star search is put on hold
    #honestly idk if this one gonna work
    def a_star(self, graph, start_node, heuristic, cost_function):
      open_list = [(0,start_node)]
      closed_set = set()

      while open_list:
        f, current_node = heapq.heappop(open_list)

        closed_set.add(current_node)

        for neighbor in graph.neighbors(current_node):
          if neighbor in closed_set:
            continue
          tentative_cost = cost_function(neighbor)  # need to define heuristic and cost idk??
          if neighbor not in (item[1] for item in open_list):
            heapq.heappush(open_list, (tentative_cost + heuristic(neighbor), neighbor))

      return current_node
    
    def find_optimal_seat(self, graph, agent):

      #TODO find a heuristic and cost function
        optimal_seat = a_star(graph, agent.cur_node, heuristic_function, cost_function)
        seat_score = cost_function(optimal_seat)
        if seat_score < agent.min_desirability_threshold:
          agent.model.schedule.remove(self)
          return None

        if optimal_seat is unavailable: # idk here need line up with code
          agent.cur_node = optimal_seat
          optimal_seat = a_star(graph, agent.cur_node, heuristic_function, cost_function)

        return optimal_seat
    
    '''

    def step(self):
        # Create agents, where number of agents follows Poisson distribution
        num_agents = self.entry_dist[self._curr_step]
        for i in range(np.random.poisson(num_agents)):
            agent = LibAgent(f'{self._curr_step}-{i}', self)
            # print(agent.unique_id, 'created!') # for debugging

            optimal_seat = self.find_optimal_seat(agent, 0.7)
            if optimal_seat is not None:
                agent.chosen_seat = optimal_seat[0]
                agent.satisfaction = optimal_seat[1]
                self.library_graph.nodes[optimal_seat]['capacity'] -= 1
                self.schedule.add(agent) # add to schedule
        
        self.datacollector.collect(self)
        node_capacities = {node: self.library_graph.nodes[node]['capacity'] for node in self.library_graph.nodes if 'capacity' in self.library_graph.nodes[node]}
        self.datacollector.collect(self, {"capacity_data": node_capacities})
        
        
        self.schedule.step()
        self._curr_step += 1

        
        


    def run(self):
        for i in range(self.total_steps):
            self.step()