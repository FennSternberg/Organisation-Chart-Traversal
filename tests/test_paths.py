import os
import unittest

from src.organization import Organization

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CASE_DIR = os.path.join(BASE_DIR, "test_inputs")


def load_org(case_filename: str) -> Organization:
    return Organization(os.path.join(CASE_DIR, case_filename))


class TestPathsExample(unittest.TestCase):
    def test_batman_to_super_ted(self):
        org = load_org("superheroes.txt")
        a_ids = org.find_employee_ids_by_name("Batman")
        b_ids = org.find_employee_ids_by_name("Super Ted")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) <- Invisible Woman (3) <- Super Ted (15)",
        )

    def test_batman_to_catwoman(self):
        org = load_org("superheroes.txt")
        a_ids = org.find_employee_ids_by_name("Batman")
        b_ids = org.find_employee_ids_by_name("Catwoman")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Batman (16) -> Black Widow (6) <- Catwoman (17)",
        )
