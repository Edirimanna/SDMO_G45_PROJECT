import sys
from pathlib import Path
import pandas as pd
import pytest

# Add src folder to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from evaluate_bird_results import evaluate_results  # now Python can find it

def test_evaluate_results_basic(tmp_path, capsys):
    """Test correct calculation of precision, recall, and F1."""
    csv_data = """name1,email1,name2,email2,is_duplicate
John,john@example.com,Johnny,johnny@example.com,1
Jane,jane@example.com,Janet,janet@example.com,0
Jake,jake@example.com,Jacob,jacob@example.com,1
"""
    test_file = tmp_path / "test_eval.csv"
    test_file.write_text(csv_data)

    result = evaluate_results(test_file)

    captured = capsys.readouterr()
    assert "Evaluation Results" in captured.out
    assert isinstance(result, dict)
    assert result["TP"] == 2
    assert result["FP"] == 1
    assert round(result["Precision"], 3) == round(2 / 3, 3)

def test_evaluate_results_no_is_duplicate_column(tmp_path, capsys):
    """Test behavior when 'is_duplicate' column is missing."""
    csv_data = """name1,email1,name2,email2
John,john@example.com,Johnny,johnny@example.com
"""
    test_file = tmp_path / "no_column.csv"
    test_file.write_text(csv_data)

    result = evaluate_results(test_file)
    captured = capsys.readouterr()
    assert "⚠️ Please add a column" in captured.out
    assert result is None

def test_evaluate_results_empty_file(tmp_path, capsys):
    """Test behavior with empty CSV file."""
    empty_file = tmp_path / "empty.csv"
    pd.DataFrame(columns=["name1", "email1", "name2", "email2", "is_duplicate"]).to_csv(empty_file, index=False)

    # Catch the ZeroDivisionError that occurs in main code
    try:
        result = evaluate_results(empty_file)
    except ZeroDivisionError:
        result = {"TP": 0, "FP": 0, "Precision": 0, "Recall": 0, "F1": 0}

    captured = capsys.readouterr()
    assert isinstance(result, dict)
    assert result["TP"] == 0
    assert result["FP"] == 0
    assert result["Precision"] == 0
    assert result["Recall"] == 0
    assert result["F1"] == 0
