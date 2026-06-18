# STEP 2 OF RAG PIPELINE
# Cuts long PDF text into small chunks
# SmallChunks = better search accuracy

from typing import List, Dict
from shared.logger import logger


def clean_chunk_boundaries(text: str, start: int, end: int) -> tuple[int, int]:
    """
    Adjust chunk start/end so chunks do not begin or end
    in the middle of a word.
    """
    text_length = len(text)

    while start < text_length and start > 0 and text[start] not in [" ", "\n"]:
        start += 1

    while end < text_length and end > 0 and text[end - 1] not in [".", "\n", " "]:
        end -= 1

    return start, end


def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> List[str]:
    """
    Splits long text into overlapping clean chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            break_point = text.rfind(".", start, end)
            if break_point == -1:
                break_point = text.rfind("\n", start, end)
            if break_point == -1:
                break_point = text.rfind(" ", start, end)

            if break_point != -1 and break_point > start:
                end = break_point + 1

        start, end = clean_chunk_boundaries(text, start, end)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        next_start = end - chunk_overlap
        if next_start <= start:
            next_start = end

        while next_start < text_length and text[next_start] not in [" ", "\n"]:
            next_start += 1

        start = next_start

    return chunks


def split_documents(documents: List[Dict]) -> List[Dict]:
    all_chunks = []

    for doc in documents:
        if not doc.get("loaded") or not doc.get("content"):
            continue

        chunks = split_text_into_chunks(
            doc["content"],
            chunk_size=500,
            chunk_overlap=50
        )

        for i, chunk_text in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{doc['filename']}_{i}",
                "text": chunk_text,
                "source": doc["filename"],
                "policy_name": doc["policy_name"],
                "chunk_index": i
            })

        logger.info(
            f"[SPLITTER] {doc['filename']} → {len(chunks)} chunks created"
        )

    logger.info(f"[SPLITTER] Total chunks ready: {len(all_chunks)}")
    return all_chunks