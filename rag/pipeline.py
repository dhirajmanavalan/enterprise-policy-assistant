# MAIN RAG PIPELINE CONTROLLER
# Connects all RAG steps together

from rag.document_loader import load_all_policies
from rag.text_splitter import split_documents
from rag.embedding_service import embed_chunks
from rag.vector_store import store_embeddings, reset_collection
from rag.retriever import retrieve_relevant_chunks, build_context_from_chunks
from shared.logger import logger


def ingest_documents():
    """
    Full indexing pipeline:
    1. Load policy PDFs
    2. Split text into chunks
    3. Convert chunks into embeddings
    4. Store embeddings in ChromaDB
    """
    logger.info("[PIPELINE] Starting document ingestion pipeline...")

    documents = load_all_policies()
    chunks = split_documents(documents)
    embedded_chunks = embed_chunks(chunks)

    reset_collection()
    store_embeddings(embedded_chunks)

    logger.info("[PIPELINE] Document ingestion completed successfully")


def query_rag(query: str, top_k: int = 3) -> str:
    """
    Full retrieval pipeline for user query:
    1. Search vector DB
    2. Collect top relevant chunks
    3. Build one context block
    """
    logger.info(f"[PIPELINE] Running RAG query pipeline for: {query}")

    chunks = retrieve_relevant_chunks(query, top_k=top_k)
    context = build_context_from_chunks(chunks)

    logger.info("[PIPELINE] RAG query pipeline completed")
    return context