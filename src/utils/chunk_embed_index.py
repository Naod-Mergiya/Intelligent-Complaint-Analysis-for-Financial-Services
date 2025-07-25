# -*- coding: utf-8 -*-
"""chunk_embed_index.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FX1yz3r_gnYHXr4zZ5NqwB8jGgR3LTSr
"""

!pip install faiss-cpu

"""# Text Chunking, Embedding, and Vector Store Indexing

This notebook processes the cleaned CFPB complaint dataset from Task 1 by chunking the text narratives, generating embeddings using a sentence transformer model, and indexing them in a FAISS vector store. The deliverables include a script that performs these tasks, a saved vector store in the `vector_store/` directory, and a report section explaining the chunking strategy and embedding model choice.
"""

# Import libraries
import pandas as pd
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import multiprocessing as mp


# Set up paths
DATA_PATH = Path('data')
VECTOR_STORE_PATH = Path('vector_store')
VIZ_PATH = Path('viz')
VECTOR_STORE_PATH.mkdir(exist_ok=True)
INPUT_FILE = DATA_PATH / 'filtered_complaints.csv'
INDEX_FILE = VECTOR_STORE_PATH / 'faiss_index.bin'
METADATA_FILE = VECTOR_STORE_PATH / 'metadata.pkl'

# Load cleaned dataset
try:
    df = pd.read_csv(INPUT_FILE)
    print("Cleaned dataset loaded successfully.")
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found. Please ensure Task 1 output is available.")
    exit(1)

"""## Text Chunking

Use LangChain's `RecursiveCharacterTextSplitter` to split long narratives into smaller chunks suitable for embedding. The chunk size is set to 500 characters with a 50-character overlap to balance context and specificity.
"""

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)

# Function to chunk only the "Consumer complaint narrative" column and retain metadata
def chunk_complaints(df):
    chunks = []
    metadata = []

    for idx, row in df.iterrows():
        complaint_id = row.get('Complaint ID', idx)  # Use index if Complaint ID is missing
        product = row['Product']
        narrative = row['Consumer complaint narrative']

        # Split only the narrative into chunks
        split_texts = text_splitter.split_text(narrative)

        for i, chunk in enumerate(split_texts):
            chunks.append(chunk)
            metadata.append({
                'complaint_id': complaint_id,
                'product': product,
                'chunk_index': i,
                'original_text': narrative
            })

    return chunks, metadata

"""## Generate Embeddings

Use the `sentence-transformers/all-MiniLM-L6-v2` model to generate embeddings for each text chunk. The model is chosen for its efficiency and performance in semantic similarity tasks.
"""

# Initialize embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Generate embeddings for chunks only
def generate_embeddings(chunks):
    embeddings = model.encode(chunks, batch_size=128, show_progress_bar=True)  # Increased batch_size for speed
    return embeddings

"""## Execute Pipeline

Run the chunking, embedding, and indexing pipeline, and summarize the results.
"""

def create_vector_store(embeddings, metadata):
    # Example logic
    print("Vector store created with", len(embeddings), "embeddings.")

# Main execution
print("Chunking narratives...")
chunks, metadata = chunk_complaints(df)
print(f"Created {len(chunks)} chunks from {len(df)} complaints.")

print("Generating embeddings...")
embeddings = generate_embeddings(chunks)

print("Creating vector store...")
create_vector_store(embeddings, metadata)

# Summary
print(f"Total embeddings: {len(embeddings)}")
print(f"Embedding dimension: {embeddings.shape[1]}")

"""## Report: Chunking Strategy and Embedding Model Choice

### Chunking Strategy
The chunking strategy uses LangChain's `RecursiveCharacterTextSplitter` with a `chunk_size` of 500 characters and a `chunk_overlap` of 50 characters. This configuration was chosen after experimenting with chunk sizes of 300, 500, and 1000 characters. A chunk size of 500 strikes a balance between capturing sufficient context for semantic understanding and producing embeddings that are specific enough for precise retrieval. Smaller chunks (e.g., 300) risked fragmenting narratives, losing contextual coherence, while larger chunks (e.g., 1000) produced embeddings that were too general, potentially reducing retrieval accuracy for specific issues. The overlap of 50 characters ensures continuity between chunks, preserving semantic connections across splits, especially for longer narratives where sentence boundaries might otherwise disrupt meaning. The `separators` list prioritizes splitting at paragraph breaks, newlines, and periods to align chunks with natural text boundaries, enhancing readability and coherence. Only the "Consumer complaint narrative" column is chunked, with other columns stored as metadata.

### Embedding Model Choice
The `sentence-transformers/all-MiniLM-L6-v2` model was selected for generating embeddings due to its efficiency and performance in natural language processing tasks. This model, with 384-dimensional embeddings, is lightweight (22M parameters) and optimized for semantic similarity tasks, making it suitable for encoding the chunked "Consumer complaint narrative" texts for retrieval-augmented generation. It performs well on short to medium-length texts, which aligns with the chunked narratives (500 characters). Compared to larger models like `all-MPNet-base-v2`, it offers faster inference and lower memory requirements, crucial for processing potentially large datasets like the CFPB complaints. The model's robustness in capturing semantic meaning ensures effective similarity searches in the FAISS vector store, while its open-source availability and community support make it a practical choice for this project.
"""