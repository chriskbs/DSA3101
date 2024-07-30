import unittest
from mesa import Agent
import pandas as pd
from unittest.mock import Mock
from lib_sections import dict_to_graph
from lib_model import LibModel
from lib_agent import LibAgent, GATE_PROBS, PREFS_PROBS, USUAL_TIMESPENT_PROBS, EXAM_TIMESPENT_PROBS
import json
lib_sections_file = open('static/lib_sections.json')
lib_sections = json.load(lib_sections_file)
sections_attrs_file = open('static/sections_attrs.json')
sections_attrs = json.load(sections_attrs_file)
connections_file = open('static/connections.json')
connections = json.load(connections_file)
df = pd.read_csv('data/20230413_clb_taps.csv')
lib_graph = dict_to_graph(lib_sections, sections_attrs, connections)

# Define mock values
mocked_timesteps = 5
mocked_optimal_seat = ("mocked_seat", 0.9)


class TestLibAgent(unittest.TestCase):
    def setUp(self):
        self.model = LibModel(df, lib_graph)
        self.agent = LibAgent("test_agent", self.model)

    def test_agent_initialization(self):
        self.assertEqual(self.agent.ID, "test_agent")
        self.assertEqual(self.agent.exam_period, self.model.exam_period)
        self.assertEqual(self.agent.min_desirability_threshold, 0)
        self.assertIsNotNone(self.agent.timesteps)
        self.assertIsNone(self.agent.chosen_seat)
        self.assertIsNone(self.agent.satisfaction)
        self.assertIsNotNone(self.agent.gate)


    def test_get_random_timesteps(self):
        # Test the get_random_timesteps method
        timesteps = self.agent.get_random_timesteps()


    def test_generate_time(self):
        # Test the generate_time method with various probability distributions
        duration = self.agent.generate_time(USUAL_TIMESPENT_PROBS)

    def test_step(self):
        # Test the step method
        with unittest.mock.patch.object(self.agent, 'get_random_timesteps', return_value=mocked_timesteps):
            with unittest.mock.patch.object(self.model, 'find_optimal_seat', return_value=mocked_optimal_seat):
                self.agent.step()

if __name__ == '__main__':
    unittest.main()