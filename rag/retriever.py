# STEP 5 OF RAG PIPELINE
# Searches ChromaDB for relevant policy chunks
# based on user query

from typing import List, Dict
from rag.embedding_service import embed_text
from rag.vector_store import get_or_create_collection
from shared.logger import logger


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> List[Dict]:
    """
    Searches ChromaDB and returns the top matching chunks.

    Input:
    - query: user question
    - top_k: how many best chunks to return

    Output:
    [
        {
            "text": "...",
            "source": "leave_policy.pdf",
            "policy_name": "Leave Policy",
            "chunk_index": 0
        }
    ]
    """
    collection = get_or_create_collection()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for doc, meta in zip(documents, metadatas):
        retrieved_chunks.append({
            "text": doc,
            "source": meta.get("source"),
            "policy_name": meta.get("policy_name"),
            "chunk_index": meta.get("chunk_index")
        })

    logger.info(
        f"[RETRIEVER] Retrieved {len(retrieved_chunks)} chunks for query: {query}"
    )

    return retrieved_chunks


def build_context_from_chunks(chunks: List[Dict]) -> str:
    """
    Converts retrieved chunks into one context block
    for the Policy RAG Agent / LLM prompt.txt.
    """
    if not chunks:
        return "No relevant policy context found."

    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['policy_name']} | {chunk['source']} | Chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}\n"
        )

    return "\n".join(context_parts)