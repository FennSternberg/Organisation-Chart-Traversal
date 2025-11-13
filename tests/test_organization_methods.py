import os
import unittest
from src.organization import Organization

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CASE_DIR = os.path.join(BASE_DIR, "tests\\test_inputs")

def load_org(case_filename: str) -> Organization:
    return Organization(os.path.join(CASE_DIR, case_filename))

class TestRoots(unittest.TestCase):
    def test_superheroes(self):
        org = load_org("superheroes.txt")
        self.assertEqual(org.roots(), [1])
        
    def test_multiple_roots(self):
        org = load_org("superheroes_multiple_roots.txt")
        self.assertEqual(org.roots(), [1, 3])


class TestFindEmployeesByName(unittest.TestCase):
    org = load_org("superheroes_spaces_and_caps.txt")
    def test_superheroes(self):
        self.org = load_org("superheroes_spaces_and_caps.txt")
        self.assertEqual(self.org.find_employee_ids_by_name("Gonzo the Great"), [2])
    
    def test_superheroes_caps(self):
        self.org = load_org("superheroes_spaces_and_caps.txt")
        self.assertEqual(self.org.find_employee_ids_by_name("gonzo the GREAT"), [2])
    
    def test_superheroes_spaces(self):
        self.org = load_org("superheroes_spaces_and_caps.txt")
        self.assertEqual(self.org.find_employee_ids_by_name(" Gonzo the Great "), [2])
    
    def test_superheroes_different(self):
        self.org = load_org("superheroes_spaces_and_caps.txt")
        self.assertEqual(self.org.find_employee_ids_by_name("Gon Zot Heg Reat"), [18])

class TestGetChainToRoot(unittest.TestCase):
    def test_superheroes(self):
        org = load_org("superheroes.txt")
        self.assertEqual(org.get_chain_to_root(16), [16, 6, 2, 1])
        self.assertEqual(org.get_chain_to_root(12), [12, 3, 1])
        self.assertEqual(org.get_chain_to_root(1), [1])
    
    def test_cyclic(self):
        """Test that cyclic management references do not cause infinite loops.
        Instead error is raised."""
        org = load_org("superheroes_cyclic.txt")
        with self.assertRaises(ValueError):
            org.get_chain_to_root(6)

class TestLCAFromChains(unittest.TestCase):
    def test_superheroes(self):
        org = load_org("superheroes.txt")
        chain_16 = org.get_chain_to_root(16)  # Batman [16, 6, 2, 1]
        chain_17 = org.get_chain_to_root(17)  # Catwoman [17, 6, 2, 1]
        lca = org._lca_from_chains(chain_16, chain_17)
        self.assertEqual(lca, 6)  # Black Widow
        chain_15 = org.get_chain_to_root(15)  # Super Ted [15, 3, 1]
        lca = org._lca_from_chains(chain_16, chain_15)
        self.assertEqual(lca, 1)  # Danger Mouse