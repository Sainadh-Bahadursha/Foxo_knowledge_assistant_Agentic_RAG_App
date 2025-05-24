from tools.file_loader import FileLoader
from vectorstore.indexer import FAISSIndexer

# 1. Load local documents (PDFs and TXTs)
documents = FileLoader([
    "data/nutrition_exercise_stress_management_for_preventing_psychiatric_diseases.pdf",
    "data/sleep_info.pdf",
    "data/community_logs.txt"
]).load_all()

# 2. Create the vector index
indexer = FAISSIndexer(persist_dir="vectorstore")
indexer.create_faiss_index(documents, index_name="company_knowledge_index")

print("✅ Vector store created at: vector_store/company_knowledge_index")
