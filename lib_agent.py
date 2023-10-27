import numpy as np
import pandas as pd
import mesa
import networkx as nx

class LibraryUser(mesa.Agent):
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.ID = unique_id
    self.timestamps = {'entry': [], 'exit': []} # why need timestamps ah?
    self.seat_type_preference = [] #TODO: need to implement distribution
                                   #e.g.
    self.min_desirability_threshold = 0
    self.timesteps = np.random.uniform(1,20) # TODO: distribution of time spent in library given enter time
    self.chosen_seat = None
    self.satisfaction = 0
    self.gate = 1 #TODO: gate enter distribution

    # self.level_pref = 0
    # self.privacy_pref = 0
    # self.crowd_level_pref = 0
    # self.comfort_pref = 0
    # self.scenery_pref = 0
    # self.lighting_pref = 0
    # self.ease_find_pref = 0
    # self.isalone = True

  def step(self):
    if self.timesteps > 0:
        self.timesteps -= 1
    else:
        self.model.schedule.remove(self)
        # TODO: remove from grid/network