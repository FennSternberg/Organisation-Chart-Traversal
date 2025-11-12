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

class TestMultipleRoots(unittest.TestCase):
    def test_multiple_roots_no_path(self):
        """
        Test that when there are multiple roots (missing manager ID's) and no path exists between two employees,
        an error is raised.
        """
        org = load_org("superheroes_multiple_roots.txt")
        # Two roots expected: 1 and 50
        roots = org.roots()
        self.assertEqual(roots, [1, 3])
        a_id = org.find_employee_ids_by_name("Batman")[0]
        b_id = org.find_employee_ids_by_name("Hit Girl")[0]
        with self.assertRaises(ValueError):
            org.format_path_between(a_id, b_id)

    
    def test_multiple_roots_path_exists(self):

        """
        Test that when there are multiple roots (missing manager ID's) and a path exists between two employees,
        the path is formatted correctly.
        """
        org = load_org("superheroes_multiple_roots.txt")
        a_ids = org.find_employee_ids_by_name("Super Ted")
        b_ids = org.find_employee_ids_by_name("Hit Girl")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Super Ted (15) -> Invisible Woman (3) <- Hit Girl (12)",
        )