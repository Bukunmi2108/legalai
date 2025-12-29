from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore = FAISS.load_local(
    "data/faiss/index", 
    embeddings=embeddings, 
    allow_dangerous_deserialization=True
)

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
compressor = FlashrankRerank(top_n=10)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, 
    base_retriever=base_retriever
)

def retrieve_reranked_documents(query):
    """Retrieve and rerank documents for a given query."""
    results = compression_retriever.invoke(query)
    return results

if __name__ == "__main__":
    sample_query = "draft a contract for software development services"
    
    reranked_docs = retrieve_reranked_documents(sample_query)
    print(f"Top Reranked documents for the query: '{sample_query}'\n")
    
    for i, doc in enumerate(reranked_docs, 1):
        score = doc.metadata.get("relevance_score", "N/A")
        print(f"Rank {i} (Score: {score}):\n{doc.page_content[:300]}...") 
        print(f"{'-'*50}\n")
    
    print("Retrieval and reranking complete.")
