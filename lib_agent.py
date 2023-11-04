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
usual_prob = pd.read_csv('notebooks/duration_counts.csv', index_col=0)
exam_prob = pd.read_csv('notebooks/duration_counts_exam.csv', index_col=0)

class LibAgent(mesa.Agent):
  def __init__(self, unique_id, model, exam_period=False):
    super().__init__(unique_id, model)

    self.ID = unique_id
    self.exam_period = exam_period
    self.min_desirability_threshold = 0
    self.timesteps = self.get_random_timesteps() # TODO: distribution of time spent in library given enter time
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
  
  def get_random_timesteps(self):
    if self.exam_period:
      return self.generate_time(exam_prob)
    else:
      return self.generate_time(usual_prob)

  def generate_time(self, prob):
    durations = prob.index
    probabilities = prob.values
    #which category it falls under
    chosen_duration = np.random.choice(durations, p=probabilities)
    #uniform distribution
    if chosen_duration == '0':
      return float(prob.loc[chosen_duration])
    elif chosen_duration == 'up to 1 hour':
      return np.random.uniform(0,1)
    elif chosen_duration == 'up to 2 hours':
      return np.random.uniform(1,2) 
    elif chosen_duration == 'up to 4 hours':
      return np.random.uniform(2,4)
    elif chosen_duration == 'up to 6 hours':
      return np.random.uniform(4,6)
    else:
      return np.random.uniform(6,12) #more than 6

  def step(self):
    if self.timesteps > 0:
        self.timesteps -= 1
    else:
        self.model.remove_agent_from_graph(self.chosen_seat)
        self.model.schedule.remove(self)
        