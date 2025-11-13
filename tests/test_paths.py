import os
import unittest
from src.organization import Organization

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CASE_DIR = os.path.join(BASE_DIR, "test_inputs")


def load_org(case_filename: str) -> Organization:
    return Organization(os.path.join(CASE_DIR, case_filename))


class TestSuperheroesExample(unittest.TestCase):
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

class TestRobustness(unittest.TestCase):
    def batman_to_super_ted(self, org:Organization):
        a_ids = org.find_employee_ids_by_name("Batman")
        b_ids = org.find_employee_ids_by_name("Super Ted")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) <- Invisible Woman (3) <- Super Ted (15)",
        )

    def test_order_independence(self):
        org = load_org("superheroes_shuffled.txt")
        self.batman_to_super_ted(org)

    def test_name_normalization(self):
        org = load_org("superheroes.txt")
        self.batman_to_super_ted(org)
    
    def test_messy_table(self):
        org = load_org("superheroes_messy_table.txt")
        self.batman_to_super_ted(org)
    
    def test_non_table_lines_ignored(self):
        org = load_org("superheroes_non_table_lines.txt")
        self.batman_to_super_ted(org)
    
    def test_single_case(self):
        org = load_org("superheroes.txt")
        a_ids = org.find_employee_ids_by_name("Batman")
        b_ids = org.find_employee_ids_by_name("Batman")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Batman (16)",
        )
    
    def test_missing_manager(self):
        """Test that missing manager ID raises ValueError when relevant to path."""
        org = load_org("superheroes_missing_manager.txt")
        a_id = org.find_employee_ids_by_name("Batman")[0]
        b_id = org.find_employee_ids_by_name("Dangermouse")[0]
        with self.assertRaises(ValueError):
            org.format_path_between(a_id, b_id)
        
    def test_missing_manager_still_works_if_irrelevant(self):
        """Test that missing manager ID does not prevent path formatting if not relevant."""
        org = load_org("superheroes_missing_manager.txt")
        a_id = org.find_employee_ids_by_name("Catwoman")[0]
        b_id = org.find_employee_ids_by_name("Dangermouse")[0]
        path = org.format_path_between(a_id, b_id)
        self.assertEqual(
            path,
            "Catwoman (17) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1)",
        )
    
    def test_not_equivalent(self):
        """Test that names which are not equivalent do not match."""
        org = load_org("superheroes_spaces_and_caps.txt")
        a_ids = org.find_employee_ids_by_name("Gonzo the Great")
        b_ids = org.find_employee_ids_by_name("gon Zot Heg Reat")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Gonzo the Great (2) <- Black Widow (6) <- Gon Zot Heg Reat (18)",
        )

    def test_equivalent(self):
        """Test that names which are equivalent match correctly."""
        org = load_org("superheroes_spaces_and_caps.txt")
        a_ids = org.find_employee_ids_by_name("batman")
        b_ids = org.find_employee_ids_by_name("gonzo the GREAT")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Batman (16) -> Black Widow (6) -> Gonzo the Great (2)",
        )

    def test_equivalent_with_extra_spaces(self):
        """Test that names which are equivalent with extra spaces match correctly."""
        org = load_org("superheroes_spaces_and_caps.txt")
        a_ids = org.find_employee_ids_by_name("  BATMAN   ")
        b_ids = org.find_employee_ids_by_name(" Gonzo   the Great ")
        path = org.format_path_between(a_ids[0], b_ids[0])
        self.assertEqual(
            path,
            "Batman (16) -> Black Widow (6) -> Gonzo the Great (2)",
        )

class TestSingleChain(unittest.TestCase):
    """
    Test organization that is a single chain (each employee has exactly one manager,
    except the root).
    """
    def test_down_chain(self):
        org = load_org("single_chain.txt")
        a_id = org.find_employee_ids_by_name("Node1")[0]
        b_id = org.find_employee_ids_by_name("Node5")[0]
        path = org.format_path_between(a_id, b_id)
        self.assertEqual(
            path,
            "Node1 (1) <- Node2 (2) <- Node3 (3) <- Node4 (4) <- Node5 (5)",
        )
    
    def test_up_chain(self):
        org = load_org("single_chain.txt")
        a_id = org.find_employee_ids_by_name("Node5")[0]
        b_id = org.find_employee_ids_by_name("Node1")[0]
        path = org.format_path_between(a_id, b_id)
        self.assertEqual(
            path,
            "Node5 (5) -> Node4 (4) -> Node3 (3) -> Node2 (2) -> Node1 (1)",
        )