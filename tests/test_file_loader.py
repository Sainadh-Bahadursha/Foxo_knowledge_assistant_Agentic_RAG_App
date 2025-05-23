import os
from tools.file_loader import FileLoader
from pprint import pprint

# Create a sample file list (update with real paths on your system)
sample_files = [
    "data/nutrition_exercise_stress_management_for_preventing_psychiatric_diseases.pdf",
    "data/sleep_info.pdf",
    "data/community_logs.txt"
]

# Ensure files exist
for file in sample_files:
    if not os.path.exists(file):
        print(f"❌ File not found: {file}")
        exit(1)

# Load documents
loader = FileLoader(sample_files)
documents = loader.load_all()

# Print result
print(f"✅ Total documents loaded: {len(documents)}/n")
for doc in documents:
    print("-" * 80)
    pprint(str(doc)[:500])
