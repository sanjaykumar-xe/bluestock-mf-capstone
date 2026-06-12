"""
Bluestock Mutual Fund Capstone
Master Pipeline Runner
"""

import os

scripts = [
    "scripts/data_ingestion.py",
    "scripts/data_cleaning.py",
    "scripts/load_to_sqlite.py",
    "scripts/performance_analytics.py",
    "scripts/advanced_analytics.py"
]

for script in scripts:
    print(f"\nRunning: {script}")
    os.system(f'python "{script}"')

print("\nPipeline Execution Complete")