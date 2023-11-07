import numpy as np
import pandas as pd
import mesa
import networkx as nx
from lib_agent import LibAgent

def compute_agents(model):
    # Calculate the total number of agents in the model
    return len(model.schedule.agents)

''' can ignore this function for now
def compute_empty_seats(model):
    # Calculate the number of empty seats in the model
    return {node: model.library_graph.nodes[node]['empty_seats'] for node in model.library_graph.nodes if 'empty_seats' in model.library_graph.nodes[node]}
'''

class LibModel(mesa.Model):
    ''' A model representing library simulation with individual agents and seating preferences '''

    def __init__(self, df, library_graph, exam_period=False):
        '''
        Initialize the library model.

        Args:
        - df (pandas DataFrame): contains entry logs and counts from the library
        - library_graph (networkx graph): represents the library floor layout and seating arrangements
        '''

        # Data preprocessing from input DataFrame
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        entry_df = df.set_index('Datetime')
        entry_df = entry_df[entry_df['Direction']=='Entry']['Direction'].resample('10min',  label='left').count().reset_index()
        entry_df.columns = ['timestamp', 'entry_counts']   # Aggregate entries every 10 mins

        # Attributes and initialization
        self.exam_period = exam_period
        self.schedule = mesa.time.RandomActivation(self) # schedule for agent activation
        self._curr_step = 0 # current simulation timestep
        self.entry_dist = entry_df.to_dict()['entry_counts'] # entry distribution over time
        self.timestamps = entry_df.to_dict()['timestamp'] # timestamps for steps
        self.total_steps = len(self.entry_dist) # total simulation steps taken
        self.library_graph = library_graph # Library layout represented as a graph

        # Data collection for reporting and analysis
        self.datacollector = mesa.DataCollector(
            model_reporters={"num_agents": compute_agents},
            agent_reporters={"chosen_seat": "chosen_seat", "satisfaction": "satisfaction"},
            tables={"SectionsData":["timestamp", "section", "level", "seat_type", "capacity", "empty_seats"]}
        )

    def remove_agent_from_graph(self, agent_node):
        '''
        Remove an agent from the library graph.

        Args:
        - agent_node(str): Node where the agent was seated  
        '''
        if self.library_graph.has_node(agent_node):
           # increases number of empty seats where the agent was seated, reflecting an agent leaving the library
           self.library_graph.nodes[agent_node]['empty_seats'] +=1

    def find_optimal_seat(self, agent, distance_weight):
        '''
        Find the optimal seat for an agent based on preferences and seat availability.

        Args:
        - agent (LibAgent): Agent for seat selection
        - distance_weight (int): Weightage for distance preference

        Returns:
        - str or None: Optimal seat node or None if no suitable seat found
        '''

        # Dictionary to store calculated path costs for available seats
        path_costs = {}

        # Iterating through the nodes in the library to find the bes avaiable seat
        for node in self.library_graph.nodes:
          # Check if the node has available seats
          if 'empty_seats' in self.library_graph.nodes[node]:
            if self.library_graph.nodes[node]['empty_seats'] > 0:
                '''path no longer necessary for model
                # Finding the shortest path from the agent's gate to the current node
                path = nx.shortest_path(self.library_graph, source=agent.gate, target=node)
                '''
                # Calculating path length from the agent's gate to the current node
                path_length = nx.shortest_path_length(self.library_graph, source=agent.gate, target=node)
                
                ''' Calculating the seat desirability score based on agent preferences and seat availability
                
                Agent will prefer those seats/sections with:
                 - high comfort, scenery, lighting, ease_find
                 - low crowd level (i.e. sections with low seat utilization rate)
                
                The final seat score is calculated by taking weighted avg w.r.t the agent preferences

                '''
                seat_score = self.library_graph.nodes[node]['privacy'] * agent.privacy_pref + \
                    self.library_graph.nodes[node]['comfort'] * agent.comfort_pref + \
                    5*self.library_graph.nodes[node]['empty_seats']/self.library_graph.nodes[node]['capacity'] * agent.crowd_level_pref + \
                    self.library_graph.nodes[node]['scenery'] * agent.scenery_pref + \
                    self.library_graph.nodes[node]['lighting'] * agent.lighting_pref + \
                    self.library_graph.nodes[node]['ease_find'] * agent.ease_find_pref 
                
                # Calculating the total seat score considering distance and desirability
                # increase in path length means less desirability (inverse relationship)
                total_score = -distance_weight * path_length + seat_score

                # Storing seats with a score above the minimum desirability threshold
                if total_score >= agent.min_desirability_threshold:
                    path_costs[node] = total_score

        # Sorting available seats based on their calculated scores
        sorted_nodes = sorted(path_costs.items(), key=lambda item: item[1], reverse=True)
        
        if sorted_nodes:
            # Return the seat with the highest score if available seats exist
            seat = sorted_nodes[0]
            return seat
        else:
            # Return None if no available seat that meets agent's preferences found
            return None  

    def step(self):
        '''
        Performs a simulation step involving agent creation, seat selection, and data collection.

        Creates agents and assigns them optimal seats based on preferences and seat availability,
        updates seat availability in the library graph, collects data, and progresses the model by one step.
        '''
        
        # Create agents based on a Poisson distribution
        num_agents = self.entry_dist[self._curr_step]
        for i in range(np.random.poisson(num_agents)):
            agent = LibAgent(f'{self._curr_step}-{i}', self)
            # print(agent.unique_id, 'created!') # for debugging

            # find optimal seat for the agent
            optimal_seat = self.find_optimal_seat(agent, 0.7)

            # Assigning chosen seat and calculating agent satisfaction if seat exists
            # Else if no seat is found, the agent will leave the library and not be added to the simulation
            if optimal_seat is not None:
                agent.chosen_seat = optimal_seat[0] # the optimal seat node (str)
                agent.satisfaction = optimal_seat[1]/agent.avg_pref # the seat score of the node
                self.library_graph.nodes[optimal_seat[0]]['empty_seats'] -= 1 # reduce the seat availability of the node chosen
                self.schedule.add(agent) # add to schedule
        
        # Collect data from the simulation
        self.datacollector.collect(self)
         
        # Collect table data for each node in the library graph
        for node in self.library_graph.nodes:
            curr_node = self.library_graph.nodes[node]
            if 'empty_seats' in curr_node:
                curr_row = {
                    "timestamp": self.timestamps[self._curr_step], "section": node, "level":curr_node['level'], 
                    "seat_type":curr_node['seat_type'], "empty_seats": curr_node['empty_seats'], "capacity": curr_node['capacity']
                }
                self.datacollector.add_table_row("SectionsData", curr_row)

        # Progress the schedule by one step and increment the current step
        self.schedule.step()
        self._curr_step += 1

    def run(self):
        '''
        Runs the simulation model for the total number of steps.

        Executes a loop for each step, performing the `step` function for each iteration to simulate the model behavior.
        '''
        for i in range(self.total_steps):
            self.step()