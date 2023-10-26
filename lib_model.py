import numpy as np
import pandas as pd
import mesa
import networkx as nx
from lib_agent import LibAgent

def compute_agents(model):
    return len(model.schedule.agents)

class LibModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, entry_df):
        self.schedule = mesa.time.RandomActivation(self)
        self._curr_step = 0
        self.entry_dist = entry_df.to_dict()['Direction']
        self.total_steps = len(self.entry_dist) # total steps taken
        self.datacollector = mesa.DataCollector(
            model_reporters={"num_agents": compute_agents},
        )

    def step(self):
        self.datacollector.collect(self)
        # Create agents, where number of agents follows Poisson distribution
        num_agents = self.entry_dist[self._curr_step]
        for i in range(np.random.poisson(num_agents)):
            agent = LibAgent(f'{self._curr_step}-{i}', self)
            # print(agent.unique_id, 'created!') # for debugging
            self.schedule.add(agent) # add to schedule
        self.schedule.step()
        self._curr_step += 1

    def run(self):
        for i in range(self.total_steps):
            self.step()