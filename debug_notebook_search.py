import os
import json
import glob

# The directory containing the notebooks is in CollectGame.Model
# Since we are running from CollectGame.CalibrationAnalysis, we need to go up and over.
# ..\CollectGame.Model\_research_archive\experiments\experiment_B_feature_aware

base_path = os.path.dirname(os.path.abspath(__file__))
# Implementation/CollectGame.CalibrationAnalysis/../CollectGame.Model/...
target_dir = os.path.join(base_path, "..", "CollectGame.Model", "_research_archive", "experiments", "experiment_B_feature_aware")

print(f"Searching in: {target_dir}")

search_term = "target_multiplier ="
search_term2 = "0.9"

for filepath in glob.glob(os.path.join(target_dir, "*.ipynb")):
    print(f"Checking {os.path.basename(filepath)}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for cell in data.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = "".join(cell.get('source', []))
                if search_term in source or search_term2 in source:
                    print(f"\nFOUND in {os.path.basename(filepath)}:")
                    print("-" * 40)
                    print(source)
                    print("-" * 40)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
