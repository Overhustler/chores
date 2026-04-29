import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
from roster import Roster, assign_chores, reset_chores
from resident import Resident
from choreList import Chore, ChoreList

class TestRoster(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.chore_list = ChoreList("All Chores", os.path.join(base_dir, "choreTest.txt"))
        self.residents = [Resident(f"Resident{i}", "Test", self.chore_list) for i in range(5)]
        self.roster = Roster(self.residents, self.chore_list)
    
    
    def test_add_resident(self):
        new_resident = Resident("Jane", "Doe", self.chore_list)
        self.roster.add_resident(new_resident)
        self.assertIn(new_resident, self.roster.residents)
        self.assertEqual(len(self.roster.residents), 6)

    def test_remove_resident(self):
        resident_to_remove = self.residents[0]
        self.roster.remove_resident(resident_to_remove)
        self.assertNotIn(resident_to_remove, self.roster.residents)
        self.assertEqual(len(self.roster.residents), 4)

    def test_update_resident_list_adds(self):
        new_resident = Resident("Jane", "Doe", self.chore_list)
        new_list = self.residents + [new_resident]
        self.roster.update_resident_list(new_list)
        self.assertIn(new_resident, self.roster.residents)
        self.assertEqual(len(self.roster.residents), 6)

    def test_update_resident_list_removes(self):
        new_list = self.residents[1:]
        self.roster.update_resident_list(new_list)
        self.assertNotIn(self.residents[0], self.roster.residents)
        self.assertEqual(len(self.roster.residents), 4)

    def test_assign_chores(self):
        assign_chores(self.roster)
        for chore in self.roster.ChoreList.getChores():
            self.assertIsNotNone(chore.get_person_assigned())

    def test_reset_chores(self):
        assign_chores(self.roster)
        reset_chores(self.roster)
        for chore in self.roster.ChoreList.getChores():
            self.assertIsNone(chore.get_person_assigned())