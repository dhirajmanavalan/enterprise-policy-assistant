# RUNS THE FULL RAG INGESTION PROCESS
# Loads policies -> splits -> embeds -> stores

from rag.pipeline import ingest_documents
from shared.logger import logger


if __name__ == "__main__":
    logger.info("[INGEST] Starting policy ingestion...")
    ingest_documents()
    logger.info("[INGEST] Policy ingestion finished.")