import unittest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.compare_heuristics import evaluate  # import from src

class TestCompareHeuristics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create temporary test CSVs folder
        cls.test_dir = Path("test_data")
        cls.test_dir.mkdir(exist_ok=True)

        # Bird heuristic test data
        cls.bird_file = cls.test_dir / "bird_test.csv"
        bird_data = pd.DataFrame({
            "name1": ["Alice", "Bob", "Charlie"],
            "email1": ["alice@example.com", "bob@example.com", "charlie@example.com"],
            "name2": ["Alicia", "Bob", "Charles"],
            "email2": ["alice123@example.com", "bob123@example.com", "charles@example.com"],
            "is_duplicate": [1, 1, 0]
        })
        bird_data.to_csv(cls.bird_file, index=False)

        # Improved heuristic test data
        cls.improved_file = cls.test_dir / "improved_test.csv"
        improved_data = pd.DataFrame({
            "name1": ["Alice", "Bob", "Charlie"],
            "email1": ["alice@example.com", "bob@example.com", "charlie@example.com"],
            "name2": ["Alice", "Bob", "Charlie"],
            "email2": ["alice@example.com", "bob@example.com", "charlie@example.com"],
            "is_duplicate": [1, 1, 1]
        })
        improved_data.to_csv(cls.improved_file, index=False)

    @classmethod
    def tearDownClass(cls):
        # Remove test files and folder
        for f in cls.test_dir.iterdir():
            f.unlink()
        cls.test_dir.rmdir()

    def test_bird_evaluation(self):
        result = evaluate(self.bird_file, label="Bird Heuristic")
        self.assertEqual(result['TP'], 2)
        self.assertEqual(result['FP'], 1)
        self.assertAlmostEqual(round(result['Precision'], 3), round(2/3, 3))


    def test_improved_evaluation(self):
        result = evaluate(self.improved_file, label="Improved Heuristic")
        self.assertEqual(result['TP'], 3)
        self.assertEqual(result['FP'], 0)
        self.assertAlmostEqual(result['Precision'], 1.0)
        self.assertAlmostEqual(result['Recall'], 1.0)
        self.assertAlmostEqual(result['F1'], 1.0)

if __name__ == "__main__":
    unittest.main()
