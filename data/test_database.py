import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import sqlite3
from choreList import Chore, ChoreList
from resident import Resident
from database import initialize_db, ChoreListRepository, ResidentRepository, increment_all_ages, DB_PATH

TEST_DB = os.path.join(os.path.dirname(__file__), "test_chores.db")

class TestChoreListRepository(unittest.TestCase):
    def setUp(self):
        initialize_db(TEST_DB)
        self.repo = ChoreListRepository(TEST_DB)
        base_dir = os.path.dirname(__file__)
        self.chore_list = ChoreList("All Chores", os.path.join(base_dir, "choreTest.txt"))

    def tearDown(self):
        with sqlite3.connect(TEST_DB) as conn:
            conn.executescript("""
                DELETE FROM last_week_chores;
                DELETE FROM restrictions;
                DELETE FROM residents;
                DELETE FROM chores;
            """)

    def test_save_and_load(self):
        self.repo.save(self.chore_list)
        loaded = self.repo.load("All Chores")
        self.assertEqual(len(loaded.getChores()), len(self.chore_list.getChores()))

    def test_chore_names_preserved(self):
        self.repo.save(self.chore_list)
        loaded = self.repo.load("All Chores")
        original_names = [c.get_name() for c in self.chore_list.getChores()]
        loaded_names = [c.get_name() for c in loaded.getChores()]
        self.assertEqual(original_names, loaded_names)

    def test_chore_times_preserved(self):
        self.repo.save(self.chore_list)
        loaded = self.repo.load("All Chores")
        original_times = [c.get_time() for c in self.chore_list.getChores()]
        loaded_times = [c.get_time() for c in loaded.getChores()]
        self.assertEqual(original_times, loaded_times)

    def test_save_overwrites(self):
        self.repo.save(self.chore_list)
        self.chore_list.add_chore("new chore", "AM")
        self.repo.save(self.chore_list)
        loaded = self.repo.load("All Chores")
        self.assertEqual(len(loaded.getChores()), 18)


class TestResidentRepository(unittest.TestCase):
    def setUp(self):
        initialize_db(TEST_DB)
        self.repo = ResidentRepository(TEST_DB)
        base_dir = os.path.dirname(__file__)
        self.chore_list = ChoreList("All Chores", os.path.join(base_dir, "choreTest.txt"))
        self.resident = Resident("John", "Doe", self.chore_list)
        self.age = 30

    def tearDown(self):
        with sqlite3.connect(TEST_DB) as conn:
            conn.executescript("""
                DELETE FROM last_week_chores;
                DELETE FROM restrictions;
                DELETE FROM residents;
                DELETE FROM chores;
            """)

    def test_save_and_load(self):
        self.repo.save(self.resident, self.age)
        loaded = self.repo.load("John", "Doe", self.age, self.chore_list)
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded.first_name, "John")
        self.assertEqual(loaded.last_name, "Doe")

    def test_restrictions_preserved(self):
        self.resident.resident_restriction["bathroom showers"] = True
        self.repo.save(self.resident, self.age)
        loaded = self.repo.load("John", "Doe", self.age, self.chore_list)
        self.assertIsNotNone(loaded)
        assert loaded is not None  # narrows type for Pylance
        self.assertTrue(loaded.resident_restriction["bathroom showers"])
        self.assertFalse(loaded.resident_restriction["trash"])

    def test_last_week_chores_preserved(self):
        last_week = self.chore_list.getChores()[:2]
        self.resident.set_last_week_chore_list(last_week)
        self.repo.save(self.resident, self.age)
        loaded = self.repo.load("John", "Doe", self.age, self.chore_list)
        assert loaded is not None
        loaded_names = [c.get_name() for c in loaded.get_last_week_chore_list()]
        self.assertIn(last_week[0].get_name(), loaded_names)
        self.assertIn(last_week[1].get_name(), loaded_names)

    def test_load_returns_none_for_unknown_resident(self):
        loaded = self.repo.load("Jane", "Smith", 25, self.chore_list)
        self.assertIsNone(loaded)

    def test_get_or_create_new_resident(self):
        resident = self.repo.get_or_create("Jane", "Smith", 25, self.chore_list)
        self.assertIsNotNone(resident)
        self.assertEqual(resident.first_name, "Jane")
        for restricted in resident.resident_restriction.values():
            self.assertFalse(restricted)

    def test_get_or_create_existing_resident(self):
        self.resident.resident_restriction["bathroom showers"] = True
        self.repo.save(self.resident, self.age)
        loaded = self.repo.get_or_create("John", "Doe", self.age, self.chore_list)
        self.assertTrue(loaded.resident_restriction["bathroom showers"])

    def test_save_overwrites_restrictions(self):
        self.repo.save(self.resident, self.age)
        self.resident.resident_restriction["bathroom showers"] = True
        self.repo.save(self.resident, self.age)
        loaded = self.repo.load("John", "Doe", self.age, self.chore_list)
        assert loaded is not None
        self.assertTrue(loaded.resident_restriction["bathroom showers"])

    def test_increment_all_ages(self):
        self.repo.save(self.resident, self.age)
        increment_all_ages(TEST_DB)
        loaded = self.repo.load("John", "Doe", self.age + 1, self.chore_list)
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded.first_name, "John")


if __name__ == "__main__":
    unittest.main()