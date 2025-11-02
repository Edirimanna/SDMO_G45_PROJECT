# SDMO Developer Duplicate Detection Project

**Project Name:** SDMO Developer Deduplication

**Language:** Python 3.12

**Libraries:** pandas, gitpython, rapidfuzz, unittest

---

## Project Overview

This project identifies potential duplicate developer identities in software repositories using heuristics. Duplicate detection is crucial for software analytics, contributor analysis, and cleaning developer data in large projects.

Two heuristics are implemented:

1. **BIRD Heuristic** – Original heuristic based on email prefix and name similarity.
2. **Improved Heuristic** – Weighted similarity using name and email prefixes with a flexible token-based approach.

The heuristics are evaluated using precision, recall, and F1-score.

---

## Project Structure

```
SDMO/
├── project_1/
│   ├── src/
│   │   ├── extract_developers.py       
│   │   ├── bird_heuristic.py           
│   │   ├── improved_heuristic.py       
│   │   ├── compare_heuristics.py
|   |   |__ ...   
│   ├── results/
|   |   |__ moby
|   |   |__ kubernetes
|   |   |__ tensorflow                 
│   ├── tests/
│   │   └── test_compare_heuristics.py
|   |   |__ ...
```

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
```

2. **Install dependencies**

```bash
pip install pandas gitpython rapidfuzz
```

3. Ensure Python version 3.12 or higher.

4. Prepare a local git repository to analyze and update `REPO_NAME` in scripts (`extract_developers.py`, `bird_heuristic.py`, `improved_heuristic.py`).

---

## Usage

### 1. Extract Developers

```bash
python src/extract_developers.py
```

Generates:

```
results/<REPO_NAME>/developers_raw.csv
```

### 2. Detect Duplicates

#### BIRD Heuristic

```bash
python src/bird_heuristic.py
```

#### Improved Heuristic

```bash
python src/improved_heuristic.py
```

Generates CSV outputs:

```
results/<REPO_NAME>/bird_duplicates.csv
results/<REPO_NAME>/improved_duplicates_validated.csv
```
### 3. Manually check Duplicates

```
![Manually check Duplicates](https://github.com/user-attachments/assets/e25f7cea-7435-478c-accf-2bfae74f5055)

```

### 4. Evaluate and Compare Heuristics

```bash
python src/compare_heuristics.py
```

Metrics printed: TP, FP, Precision, Recall, F1-score.

---

## Unit Testing

Run automated tests:

```bash
python -m unittest tests.test_compare_heuristics
```

---

## Results

| Heuristic          | Pairs | TP  | FP  | Precision | Recall | F1    |
| ------------------ | ----- | --- | --- | --------- | ------ | ----- |
| Bird Heuristic     | 996   | 778 | 218 | 0.781     | 1.0    | 0.877 |
| Improved Heuristic | 546   | 546 | 0   | 1.0       | 1.0    | 1.0   |

---

## Test Plan

* Verify extraction of unique developers.
* Validate duplicate detection for both heuristics.
* Evaluate metrics (TP, FP, precision, recall, F1).
* Run unit tests to ensure correctness and prevent regressions.

---

## Future Work

* Extend heuristics to better handle international names and email variations.
* Optimize performance for large repositories.
* Integrate with GitHub/GitLab APIs for live repository analysis.

---

