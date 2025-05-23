from tools.file_loader import FileLoader
from vectorstore.indexer import FAISSIndexer

loader = FileLoader([
    "data/nutrition_exercise_stress_management_for_preventing_psychiatric_diseases.pdf",
    "data/sleep_info.pdf",
    "data/community_logs.txt"
    ])
docs = loader.load_all()

indexer = FAISSIndexer()
indexer.create_faiss_index(docs, "sample_index")

retriever = indexer.load_index("sample_index")
print("✅ FAISS index loaded. Sample results:")
results = retriever.similarity_search("How much sleep do we need? Provide with respect to age.")
for r in results:
    print(r.page_content)
