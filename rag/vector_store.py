# STEP 4 OF RAG PIPELINE
# Stores embeddings in Chroma_DB
# ChromaDB = vector database for semantic search

from typing import List, Dict
import chromadb
from chromadb.config import Settings
from shared.logger import logger

CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "enterprise_policies"


def get_chroma_client():
    """
    Creates persistent ChromaDB client.
    Data will be stored locally in data/chroma_db
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client


def get_or_create_collection():
    """
    Returns ChromaDB collection for policy chunks.
    Creates it if it does not exist.
    """
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    logger.info(f"[VECTOR STORE] Using collection: {COLLECTION_NAME}")
    return collection


def store_embeddings(chunks_with_embeddings: List[Dict]) -> None:
    """
    Stores embedded chunks into ChromaDB.

    Input:
    [
        {
            "chunk_id": "...",
            "text": "...",
            "source": "...",
            "policy_name": "...",
            "chunk_index": 0,
            "embedding": [...]
        }
    ]
    """
    if not chunks_with_embeddings:
        logger.warning("[VECTOR STORE] No embeddings received to store")
        return

    collection = get_or_create_collection()

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in chunks_with_embeddings:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])
        metadatas.append({
            "source": chunk["source"],
            "policy_name": chunk["policy_name"],
            "chunk_index": chunk["chunk_index"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    logger.info(
        f"[VECTOR STORE] Stored {len(chunks_with_embeddings)} chunks in ChromaDB"
    )


def reset_collection():
    """
    Deletes old collection and recreates it.
    Useful during development/testing.
    """
    client = get_chroma_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
        logger.info(f"[VECTOR STORE] Deleted old collection: {COLLECTION_NAME}")
    except Exception:
        logger.info("[VECTOR STORE] No existing collection to delete")

    client.get_or_create_collection(name=COLLECTION_NAME)
    logger.info(f"[VECTOR STORE] Fresh collection ready: {COLLECTION_NAME}")