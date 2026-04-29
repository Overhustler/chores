import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import unittest


from choreList import ChoreList
from resident import Resident
class TestResident(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.chore_list = ChoreList("All Chores", os.path.join(base_dir, "choreTest.txt"))
        self.resident = Resident("John", "Doe", self.chore_list)
        self.chores = self.chore_list.getChores()

    def test_display_name(self):
        self.assertEqual(self.resident.getDisplayName(), "John D.")

    def test_initial_restrictions(self):
        for chore, restricted in self.resident.resident_restriction.items():
            self.assertFalse(restricted)

    def test_set_last_week_chore_list(self):
        last_week = self.chores[:2]
        self.resident.set_last_week_chore_list(last_week)
        self.assertEqual(self.resident.get_last_week_chore_list(), last_week)

    def test_last_week_chores_default_empty(self):
        self.assertEqual(self.resident.get_last_week_chore_list(), [])

    def test_restrictions_including_last_week(self):
        last_week = self.chores[:2]
        self.resident.set_last_week_chore_list(last_week)
        restrictions = self.resident.restrictions_including_last_week()
        self.assertTrue(restrictions[self.chores[0].get_name()])
        self.assertTrue(restrictions[self.chores[1].get_name()])
        self.assertFalse(restrictions[self.chores[2].get_name()])

    def test_restrictions_not_all_blocked(self):
        self.resident.set_last_week_chore_list(self.chores)
        restrictions = self.resident.restrictions_including_last_week()
        num_available = sum(1 for v in restrictions.values() if not v)
        self.assertGreater(num_available, 0)