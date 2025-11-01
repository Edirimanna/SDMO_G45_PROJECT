import sys
import os
import pandas as pd
import pytest
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from bird_heuristic import (
    normalize_text,
    extract_name_parts,
    email_prefix,
    similar,
    bird_heuristic_filtered,
)


def test_normalize_text_basic():
    assert normalize_text(" Jöhn Döe ") == "john doe"
    assert normalize_text("M@il!123") == "m@il123"
    assert normalize_text(None) == ""

def test_extract_name_parts():
    assert extract_name_parts("John Doe") == ("John", "Doe")
    assert extract_name_parts("John") == ("John", "")
    assert extract_name_parts("") == ("", "")

def test_email_prefix():
    assert email_prefix("john@example.com") == "john"
    assert email_prefix("invalidemail") == "invalidemail"
    assert email_prefix("") == ""

def test_similar_true_false():
    assert similar("john", "john", 95)
    assert not similar("john", "jane", 95)


def test_bird_heuristic_detects_duplicates(tmp_path):
    """Check that near-duplicate names/emails are detected correctly."""
    csv_data = """name,email
John Doe,john@example.com
Jöhn Döe,johnd@example.com
Jane Smith,jane@example.com
"""
    df = pd.read_csv(StringIO(csv_data))

    # Dynamically patch output path
    import bird_heuristic as bird_module
    output_file = tmp_path / "duplicates.csv"
    bird_module.OUTPUT_FILE = str(output_file)

    # Run heuristic
    result_df = bird_module.bird_heuristic_filtered(df, threshold=90)

    # Assertions
    assert isinstance(result_df, pd.DataFrame)
    assert all(col in result_df.columns for col in ["name1", "email1", "name2", "email2"])
    assert len(result_df) >= 1  # Should detect at least one duplicate

    # Check that file was written and not empty
    saved_df = pd.read_csv(output_file)
    assert not saved_df.empty

def test_bird_heuristic_no_duplicates(tmp_path):
    """Ensure distinct entries produce no duplicates."""
    csv_data = """name,email
Alice Wonderland,alice@abc.com
Bob Builder,bob@xyz.com
"""
    df = pd.read_csv(StringIO(csv_data))

    import bird_heuristic as bird_module
    bird_module.OUTPUT_FILE = str(tmp_path / "no_dupes.csv")

    result_df = bird_module.bird_heuristic_filtered(df, threshold=95)

    # Assertions
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.empty
