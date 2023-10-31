import numpy as np
import pandas as pd
import mesa
import networkx as nx

class LibraryUser(mesa.Agent):
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.ID = unique_id
    self.timestamps = {'entry': [], 'exit': []} # why need timestamps ah?
    self.seat_type_preference = [] 
    
    #TODO: need to implement distribution for the seat_type_pref
    #e.g.


    self.min_desirability_threshold = 0
    self.timesteps = np.random.uniform(1,20) #TODO: distribution of time spent in library given enter time
    self.chosen_seat = None
    self.satisfaction = 0
    

    gate_probabilities = [0.4, 0.3, 0.3]  # Probabilities for gates
    gates = ["clb_1_gate", "clb_4_gate", "wbs_6_gate"]

    self.gate = np.random.choice(gates, p=gate_probabilities)

    # need to employ distributions
    self.level_pref = np.random.uniform(1,5) # do we need
    self.privacy_pref = np.random.uniform(1,5)
    self.crowd_level_pref = np.random.uniform(1,5)
    self.comfort_pref = np.random.uniform(1,5)
    self.scenery_pref = np.random.uniform(1,5)
    self.lighting_pref = np.random.uniform(1,5)
    self.ease_find_pref = np.random.uniform(1,5) # how bout this
    self.isalone = np.random.choice([True, False], p=[0.5, 0.5]) # how bout this
  

  def step(self):
    if self.timesteps > 0:
        self.timesteps -= 1
    else:
        self.model.remove_agent_from_graph(self.chosen_seat)
        #TODO: remove from grid/network
        self.model.schedule.remove(self)
        