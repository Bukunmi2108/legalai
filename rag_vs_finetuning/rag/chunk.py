import json
import os
from tqdm import tqdm
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
JSON_FILE_PATH = "data/contracts_cleaned.json"
FAISS_INDEX_PATH = "data/faiss/index"
BATCH_SIZE = 100 
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def load_and_chunk_contracts(file_path):
    """
    Specifically optimized for the 'contracts_cleaned.json' structure.
    Injects context into every chunk to prevent 'Lost Context' during retrieval.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    docs_to_embed = []
    
    for index, item in enumerate(tqdm(data, desc="Processing Contracts")):
        # 1. Extract high-value metadata
        doc_id = item.get("doc_id", "Unknown ID")
        title = item.get("title", "Untitled Contract")
        gov_law = item.get("governing_law", "Not Specified")
        full_text = item.get("text", "")

        if not full_text:
            continue

        # 2. Split the main body text
        chunks = text_splitter.split_text(full_text)
        
        for i, chunk_text in enumerate(chunks):
            # 3. CONTEXT INJECTION
            contextual_content = (
                f"CONTRACT TITLE: {title}\n"
                f"GOVERNING LAW: {gov_law}\n"
                f"CONTENT: {chunk_text}"
            )
            
            # 4. Create Document with searchable metadata
            docs_to_embed.append(Document(
                page_content=contextual_content,
                metadata={
                    "doc_id": doc_id,
                    "title": title,
                    "row_index": index,
                    "chunk_id": i,
                    "source": file_path
                }
            ))
    
    print(f"Created {len(docs_to_embed)} contextual chunks from {len(data)} contracts.")
    return docs_to_embed

def create_vectorstore(file_path, index_path):
    all_docs = load_and_chunk_contracts(file_path)
    
    if not all_docs:
        print("No documents found to process.")
        return

    print(f"--- Initializing FAISS Index ---")
    
    # Process the first batch to initialize the index
    initial_batch = all_docs[:BATCH_SIZE]
    vectorstore = FAISS.from_documents(initial_batch, embeddings)
    
    # Process remaining in batches
    remaining_docs = all_docs[BATCH_SIZE:]
    batches = [remaining_docs[i : i + BATCH_SIZE] for i in range(0, len(remaining_docs), BATCH_SIZE)]

    for batch in tqdm(batches, desc="Generating Embeddings"):
        try:
            vectorstore.add_documents(batch)
        except Exception as e:
            print(f"Skipping failed batch: {e}")

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    
    vectorstore.save_local(index_path)
    print(f"Success! Vectorstore saved to {index_path}")

if __name__ == "__main__":
    create_vectorstore(JSON_FILE_PATH, FAISS_INDEX_PATH)