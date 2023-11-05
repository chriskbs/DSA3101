import numpy as np
import pandas as pd
import mesa
import networkx as nx

GATE_PROBS = pd.read_csv('notebooks/survey_data/dist_entry_gates.csv', index_col=0)
PREFS_PROBS = pd.read_csv('notebooks/survey_data/dist_factors.csv', index_col=0)
USUAL_TIMESPENT_PROBS = pd.read_csv('notebooks/survey_data/duration_counts.csv', index_col=0)
EXAM_TIMESPENT_PROBS = pd.read_csv('notebooks/survey_data/duration_counts_exam.csv', index_col=0)

class LibAgent(mesa.Agent):
  def __init__(self, unique_id, model, exam_period=False):
    super().__init__(unique_id, model)

    self.ID = unique_id
    self.exam_period = exam_period
    self.min_desirability_threshold = 0
    self.timesteps = self.get_random_timesteps()
    self.chosen_seat = None
    self.satisfaction = None

    self.gate = np.random.choice(GATE_PROBS.index.values, p=GATE_PROBS.probs.values)

    self.level_pref = np.random.uniform(1,5) # Ignore this level_pref for now
    self.privacy_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.privacy.values)
    self.crowd_level_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.crowd_level.values)
    self.comfort_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.comfort.values)
    self.scenery_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.scenery.values)
    self.lighting_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.lighting.values)
    self.ease_find_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.ease_to_find.values)
    self.isalone = np.random.choice([True, False], p=[0.5, 0.5]) # ignore is_alone for now

    self.avg_pref = self.privacy_pref + self.comfort_pref + self.scenery_pref + self.lighting_pref + self.ease_find_pref + self.crowd_level_pref
  
  def get_random_timesteps(self):
    if self.exam_period:
      return self.generate_time(EXAM_TIMESPENT_PROBS)
    else:
      return self.generate_time(USUAL_TIMESPENT_PROBS)

  def generate_time(self, prob):
    durations = prob.index.values
    probabilities = prob.usual_amt_time.values
    #which category it falls under
    chosen_duration = np.random.choice(durations, p=probabilities)
    #uniform distribution
    if chosen_duration == '0':
      return float(prob.loc[chosen_duration])
    elif chosen_duration == 'up to 1 hour':
      return np.random.uniform(0,1)*60/10
    elif chosen_duration == 'up to 2 hours':
      return np.random.uniform(1,2)*60/10
    elif chosen_duration == 'up to 4 hours':
      return np.random.uniform(2,4)*60/10
    elif chosen_duration == 'up to 6 hours':
      return np.random.uniform(4,6)*60/10
    else:
      return np.random.uniform(6,12)*60/10 #more than 6 hrs

  def step(self):
    if self.timesteps > 0:
        self.timesteps -= 1
    else:
        self.model.remove_agent_from_graph(self.chosen_seat)
        self.model.schedule.remove(self)
        