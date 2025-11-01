# File: SDMO/tests/test_extract_developers.py
import sys
import os
import subprocess
import pandas as pd

def test_script_creates_csv():
    # Absolute path to the script
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/extract_developers.py"))

    # Run the script in its real directory
    cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))

    result_file = os.path.join(cwd, "results", "developers_raw.csv")

    # Remove existing CSV if any
    if os.path.exists(result_file):
        os.remove(result_file)

    # Run the script
    subprocess.run([sys.executable, script_path], cwd=cwd, check=True)

    # Check if CSV was created
    assert os.path.exists(result_file), "developers_raw.csv was not created"

    # Optional: verify CSV contents
    df = pd.read_csv(result_file)
    assert "name" in df.columns
    assert "email" in df.columns
