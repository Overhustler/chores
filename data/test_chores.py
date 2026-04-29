import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import unittest
from choreList import Chore, ChoreList
from resident import Resident
from scheduler import Scheduler

class TestChoreList(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.chore_list = ChoreList("All Chores", os.path.join(base_dir, "choreTest.txt"))

    def test_chores_loaded(self):
        self.assertEqual(len(self.chore_list.getChores()), 17)

    def test_chore_names(self):
        names = [c.get_name() for c in self.chore_list.getChores()]
        self.assertIn("bathroom showers", names)
        self.assertIn("sweep/mop main", names)

    def test_add_chore(self):
        self.chore_list.add_chore("new chore", "PM")
        self.assertEqual(len(self.chore_list.getChores()), 18)

    def test_remove_chore(self):
        chore = self.chore_list.getChores()[0]
        self.chore_list.remove_chore(chore)
        self.assertEqual(len(self.chore_list.getChores()), 16)


class TestScheduler(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.chore_list = ChoreList("All Chores", os.path.join(base_dir, "choreTest.txt"))
        self.residents = [Resident(f"Resident{i}", "Test", self.chore_list) for i in range(17)]

    def test_all_chores_assigned(self):
        assignments = Scheduler.make_chore_list(self.residents, self.chore_list)
        self.assertEqual(len(assignments), 17)

    def test_no_double_assignment(self):
        assignments = Scheduler.make_chore_list(self.residents, self.chore_list)
        assigned_residents = list(assignments.values())
        # each resident should only appear once on first pass
        self.assertEqual(len(assigned_residents), len(set(assigned_residents)))

    def test_fewer_residents_than_chores(self):
        few_residents = self.residents[:8]
        assignments = Scheduler.make_chore_list(few_residents, self.chore_list)
        # some residents will have 2 chores, all chores should still be assigned
        self.assertEqual(len(assignments), 17)


if __name__ == "__main__":
    unittest.main()