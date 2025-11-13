import sys
import io
import MyProgram as cli
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CASE_DIR = os.path.join(BASE_DIR, "test_inputs")
class TestCLI(unittest.TestCase):
    def test_non_unique_names(self):
        """Test that when multiple employees share the same name, the program prompts for disambiguation."""
        path = os.path.join(CASE_DIR, "minions_non_unique.txt")

        # Save the real system input/output streams so they can be restored later.
        real_stdout, real_stdin = sys.stdout, sys.stdin
        try:
            # Redirect stdout
            sys.stdout = io.StringIO()
            # Simulate a user typing "103" and pressing Enter
            sys.stdin = io.StringIO("103\n")

            # Run the program command with the test arguments
            code = cli.main([path, "Black widow", "Minion"])
            output_lines = sys.stdout.getvalue().strip().splitlines()
        finally:
            # Restore the real system streams
            sys.stdout = real_stdout
            sys.stdin = real_stdin

        self.assertEqual(code, 0)
        self.assertTrue(output_lines)
        joined = "\n".join(output_lines)
        self.assertIn("Multiple matches found for 'Minion'", joined)
        self.assertIn("Minion (101)", joined)
        self.assertIn("Minion (102)", joined)
        self.assertIn("Minion (103)", joined)
        self.assertIn("Enter the employee ID for the second person:", joined)
        self.assertEqual(
            output_lines[-1],
            "Black Widow (107) -> Captain Marvel (105) -> Minion (102) -> Boss (100) <- Minion (103)",
        )
        
    def test_missing_name_error(self):
        path = os.path.join(CASE_DIR, "superheroes.txt")
        stderr = sys.stderr
        try:
            sys.stderr = io.StringIO()
            code = cli.main([path, "Not A Name", "Super Ted"])
        finally:
            sys.stderr = stderr
        self.assertEqual(code, 1)
