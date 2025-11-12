import os
import unittest

from src.organization import Organization


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CASE_DIR = os.path.join(BASE_DIR, "test_inputs")


def load_org(case_filename: str) -> Organization:
    return Organization(os.path.join(CASE_DIR, case_filename))


class TestInputLoading(unittest.TestCase):
    def generic_superheroes_input_check(self, org: Organization):
        self.assertEqual(len(org.employees), 8)

        self.assertEqual(org.employees[1].name_normalized, "dangermouse")
        self.assertEqual(org.employees[1].manager_id, None)
        self.assertEqual(org.get_children(1), [2, 3])
       
        self.assertEqual(org.employees[2].name_normalized, "gonzo the great")
        self.assertEqual(org.employees[2].manager_id, 1)
        self.assertEqual(org.get_children(2), [6])

        self.assertEqual(org.employees[3].name_normalized, "invisible woman")
        self.assertEqual(org.employees[3].manager_id, 1)
        self.assertEqual(org.get_children(3), [12, 15])

        self.assertEqual(org.employees[6].name_normalized, "black widow")
        self.assertEqual(org.employees[6].manager_id, 2)
        self.assertEqual(org.get_children(6), [16, 17])

        self.assertEqual(org.employees[12].name_normalized, "hit girl")
        self.assertEqual(org.employees[12].manager_id, 3)
        self.assertEqual(org.get_children(12), [])

        self.assertEqual(org.employees[15].name_normalized, "super ted")
        self.assertEqual(org.employees[15].manager_id, 3)
        self.assertEqual(org.get_children(15), [])

        self.assertEqual(org.employees[16].name_normalized, "batman")
        self.assertEqual(org.employees[16].manager_id, 6)
        self.assertEqual(org.get_children(16), [])

        self.assertEqual(org.employees[17].name_normalized, "catwoman")
        self.assertEqual(org.employees[17].manager_id, 6)
        self.assertEqual(org.get_children(17), [])


    def test_superheroes(self):
        org = load_org("superheroes.txt")
        self.generic_superheroes_input_check(org)
    
    def test_superheroes_messy_table(self):
        org = load_org("superheroes_messy_table.txt")
        self.generic_superheroes_input_check(org)
    
    def test_superheroes_shuffled(self):
        org = load_org("superheroes_shuffled.txt")
        self.generic_superheroes_input_check(org)
    
    def test_superheroes_non_table_lines(self):
        org = load_org("superheroes_non_table_lines.txt")
        self.generic_superheroes_input_check(org)