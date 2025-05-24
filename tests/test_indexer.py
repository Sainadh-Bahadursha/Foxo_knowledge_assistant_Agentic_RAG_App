from vectorstore.indexer import FAISSIndexer

# Initialize FAISS index loader
indexer = FAISSIndexer(persist_dir="vectorstore")

# Load the pre-built index (assumes it’s in vectorstore/company_knowledge_index/)
retriever = indexer.load_index("company_knowledge_index")

# Run a test query
print("✅ FAISS index loaded. Sample results:")
results = retriever.similarity_search("How much sleep do we need? Provide with respect to age.")

for r in results:
    print("-" * 80)
    print(r.page_content)
