from vectorstore.indexer import FAISSIndexer
from agents.base_agent import FOXOAgent

def main():
    print("\n🧠 Welcome to FOXO Knowledge Assistant")
    print("Type 'exit' to quit.\n")

    # Load the FAISS index
    indexer = FAISSIndexer(persist_dir="vectorstore")
    retriever = indexer.load_index("company_knowledge_index")

    # Initialize the FOXO React Agent
    agent = FOXOAgent(retriever)

    # CLI loop
    while True:
        query = input("👤 You: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            answer = agent.ask(query)
            print(f"\n🤖 FOXO: {answer}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

if __name__ == "__main__":
    main()
