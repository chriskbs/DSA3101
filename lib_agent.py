import numpy as np
import pandas as pd
import mesa
import networkx as nx

# Obtaining the distributions for agent attributes from CSV files
GATE_PROBS = pd.read_csv('notebooks/survey_data/dist_entry_gates.csv', index_col=0)
PREFS_PROBS = pd.read_csv('notebooks/survey_data/dist_factors.csv', index_col=0)
USUAL_TIMESPENT_PROBS = pd.read_csv('notebooks/survey_data/duration_counts.csv', index_col=0)
EXAM_TIMESPENT_PROBS = pd.read_csv('notebooks/survey_data/duration_counts_exam.csv', index_col=0)
LEVEL_PREF_PROBS = pd.read_csv('notebooks/survey_data/dist_lvl_rate.csv', index_col=0) #read csv file first jic need to use
IS_ALONE_PROBS = pd.read_csv('notebooks/survey_data/dist_is_alone.csv', index_col=0) #read csv file first jic need use

class LibAgent(mesa.Agent):
  ''' Represents an agent in the library simulation model. '''

  def __init__(self, unique_id, model):
    '''
    Initialize an agent in the library model.

    Args:
    - unique_id (str): Unique identifier for the agent
    - model (LibModel): Reference to the model
    - exam_period (bool): Whether it's an exam period or not
    '''
    super().__init__(unique_id, model)

    #agent attributes intitialization
    self.ID = unique_id
    self.exam_period = model.exam_period
    self.min_desirability_threshold = 0
    self.timesteps = self.get_random_timesteps()
    self.chosen_seat = None
    self.satisfaction = None

    # Attribute initialization based on probability distributions
    self.gate = np.random.choice(GATE_PROBS.index.values, p=GATE_PROBS.probs.values)
    self.level_pref = np.random.uniform(1,5) # Ignore this level_pref for now
    self.privacy_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.privacy.values)
    self.crowd_level_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.crowd_level.values)
    self.comfort_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.comfort.values)
    self.scenery_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.scenery.values)
    self.lighting_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.lighting.values)
    self.ease_find_pref = np.random.choice(PREFS_PROBS.index.values, p=PREFS_PROBS.ease_to_find.values)
    self.isalone = np.random.choice([True, False], p=[0.5, 0.5]) # ignore is_alone for now

    # calculating aggregate preference score
    self.avg_pref = (self.privacy_pref + self.comfort_pref + self.scenery_pref + 
                     self.lighting_pref + self.ease_find_pref + self.crowd_level_pref)
  
  def get_random_timesteps(self):
    ''' Choosing duration counts based on whether it is during an exam period or not. '''
    if self.exam_period:
      return self.generate_time(EXAM_TIMESPENT_PROBS)
    else:
      return self.generate_time(USUAL_TIMESPENT_PROBS)

  def generate_time(self, prob):
    ''' Generate durations based on probability distribution. '''
    durations = prob.index.values
    probabilities = prob.usual_amt_time.values
    
    # Choose the duration category
    chosen_duration = np.random.choice(durations, p=probabilities)

    # Uniformly generate time within specified durations
    if chosen_duration == '0':
      return float(prob.loc[chosen_duration])
    elif chosen_duration == 'up to 1 hour':
      return np.random.uniform(0,1) * 60 / 10
    elif chosen_duration == 'up to 2 hours':
      return np.random.uniform(1,2) * 60 / 10
    elif chosen_duration == 'up to 4 hours':
      return np.random.uniform(2,4) * 60 / 10
    elif chosen_duration == 'up to 6 hours':
      return np.random.uniform(4,6) * 60 / 10
    else:
      return np.random.uniform(6,12) * 60 / 10 #more than 6 hrs

  def step(self):
    ''' Perform a simulation step for the agent in the model. '''
    if self.timesteps > 0:
        # Reduce agent time spent in the library by 1 every step in the model.
        self.timesteps -= 1
    else:
        # If timesteps reach 0, remove agent from the graph and the model's schedule
        self.model.remove_agent_from_graph(self.chosen_seat)
        self.model.schedule.remove(self)
        