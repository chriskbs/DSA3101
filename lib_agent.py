import numpy as np
import pandas as pd
import mesa
import networkx as nx

# TODO: fill in probabilities (can be manual or using pandas to read the csv that u created)
GATE_PROBS = [0.4, 0.3, 0.3] # TODO: probabilities for gates and preferences
# PRIVACY_PROBS =
# CROWD_LEVEL_PROBS = 
# COMFORT_PROBS = 
# SCENERY_PROBS = 
# LIGHTING_PROBS = 
# EASE_FIND_PROBS = 

class LibAgent(mesa.Agent):
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)

    self.ID = unique_id

    self.min_desirability_threshold = 0
    self.timesteps = np.random.uniform(1,20) # TODO: distribution of time spent in library given enter time
    self.chosen_seat = None
    self.satisfaction = None

    gate_probabilities = GATE_PROBS
    gates = ["clb_1_gate", "clb_4_gate", "wbs_6_gate"]

    self.gate = np.random.choice(gates, p=gate_probabilities)

    # TODO: need to change to np.random.choice, using the ..._PROBS constants defined at the start
    self.level_pref = np.random.uniform(1,5) # Ignore this level_pref for now
    self.privacy_pref = np.random.uniform(1,5)
    self.crowd_level_pref = np.random.uniform(1,5)
    self.comfort_pref = np.random.uniform(1,5)
    self.scenery_pref = np.random.uniform(1,5)
    self.lighting_pref = np.random.uniform(1,5)
    self.ease_find_pref = np.random.uniform(1,5)
    self.isalone = np.random.choice([True, False], p=[0.5, 0.5]) # ignore is_alone for now

    self.avg_pref = self.privacy_pref + self.comfort_pref + self.scenery_pref + self.lighting_pref + self.ease_find_pref + self.crowd_level_pref
  

  def step(self):
    if self.timesteps > 0:
        self.timesteps -= 1
    else:
        self.model.remove_agent_from_graph(self.chosen_seat)
        self.model.schedule.remove(self)
        