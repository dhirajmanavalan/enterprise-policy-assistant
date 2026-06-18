# STEP 3 OF RAG PIPELINE
# Converts text chunks into embedding
# Embeddings = vectors used for semantic search

from typing import List, Dict
from sentence_transformers import SentenceTransformer
from shared.logger import logger

_model = None


def get_embedding_model():
    """
    Loads embedding model only once.
    Reuses same model for all chunks.
    """
    global _model

    if _model is None:
        logger.info("[EMBEDDING] Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("[EMBEDDING] Model loaded successfully")

    return _model


def embed_text(text: str) -> List[float]:
    """
    Converts a single text chunk into embedding vector.
    """
    model = get_embedding_model()
    embedding = model.encode(text).tolist()
    return embedding


def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Takes chunked documents and adds embeddings.

    Input:
    [
        {
            "chunk_id": "...",
            "text": "...",
            "source": "...",
            "policy_name": "...",
            "chunk_index": 0
        }
    ]

    Output:
    Same structure + embedding field
    """
    embedded_chunks = []
    model = get_embedding_model()

    logger.info(f"[EMBEDDING] Creating embeddings for {len(chunks)} chunks...")

    texts = [chunk["text"] for chunk in chunks]
    vectors = model.encode(texts).tolist()

    for chunk, vector in zip(chunks, vectors):
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "source": chunk["source"],
            "policy_name": chunk["policy_name"],
            "chunk_index": chunk["chunk_index"],
            "embedding": vector
        })

    logger.info(
        f"[EMBEDDING] Completed embeddings for {len(embedded_chunks)} chunks"
    )

    return embedded_chunks