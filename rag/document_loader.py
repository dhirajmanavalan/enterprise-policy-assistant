# STEP 1 OF RAG PIPELINE
# Reads policy text files from data/policies/
# Supports both .txt and .pdf files

import os
from typing import List, Dict
from shared.logger import logger
from shared.config import settings


def load_single_txt(file_path: str) -> Dict:
    """Reads one .txt policy file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        filename = os.path.basename(file_path)
        policy_name = (
            filename
            .replace(".txt", "")
            .replace(".pdf", "")
            .replace("_", " ")
            .title()
        )

        if not content:
            logger.warning(f"[LOADER] Empty TXT skipped: {filename}")
            return {
                "filename": filename,
                "policy_name": policy_name,
                "file_path": file_path,
                "content": "",
                "char_count": 0,
                "loaded": False,
                "error": "Empty text file"
            }

        logger.info(
            f"[LOADER] Loaded TXT: {filename} | "
            f"Characters: {len(content)}"
        )

        return {
            "filename": filename,
            "policy_name": policy_name,
            "file_path": file_path,
            "content": content,
            "char_count": len(content),
            "loaded": True
        }

    except Exception as e:
        logger.error(f"[LOADER] TXT Failed: {file_path} | {str(e)}")
        return {
            "filename": os.path.basename(file_path),
            "content": "",
            "loaded": False,
            "error": str(e)
        }


def load_single_pdf(file_path: str) -> Dict:
    """Reads one .pdf policy file"""
    try:
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        full_text = ""

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += f"\n[Page {page_num + 1}]\n{page_text}"

        full_text = full_text.strip()

        filename = os.path.basename(file_path)
        policy_name = (
            filename
            .replace(".pdf", "")
            .replace("_", " ")
            .title()
        )

        if not full_text:
            logger.warning(f"[LOADER] Empty PDF skipped: {filename}")
            return {
                "filename": filename,
                "policy_name": policy_name,
                "file_path": file_path,
                "content": "",
                "page_count": len(reader.pages),
                "char_count": 0,
                "loaded": False,
                "error": "Empty PDF content"
            }

        logger.info(
            f"[LOADER] Loaded PDF: {filename} | "
            f"Pages: {len(reader.pages)} | "
            f"Characters: {len(full_text)}"
        )

        return {
            "filename": filename,
            "policy_name": policy_name,
            "file_path": file_path,
            "content": full_text,
            "page_count": len(reader.pages),
            "char_count": len(full_text),
            "loaded": True
        }

    except Exception as e:
        logger.error(f"[LOADER] PDF Failed: {file_path} | {str(e)}")
        return {
            "filename": os.path.basename(file_path),
            "content": "",
            "loaded": False,
            "error": str(e)
        }


def load_all_policies() -> List[Dict]:
    """
    Loads all supported policy files from data/policies/.
    Supports:
    - .txt
    - .pdf
    """
    policies_path = settings.policy_docs_path

    if not os.path.exists(policies_path):
        logger.error(f"[LOADER] Folder not found: {policies_path}")
        return []

    supported_files = [
        f for f in os.listdir(policies_path)
        if f.endswith(".txt") or f.endswith(".pdf")
    ]

    if not supported_files:
        logger.error("[LOADER] No .txt or .pdf policy files found")
        return []

    logger.info(f"[LOADER] Found {len(supported_files)} policy files")

    documents = []

    for file_name in sorted(supported_files):
        file_path = os.path.join(policies_path, file_name)

        if file_name.endswith(".txt"):
            doc = load_single_txt(file_path)
        elif file_name.endswith(".pdf"):
            doc = load_single_pdf(file_path)
        else:
            continue

        if doc.get("loaded"):
            documents.append(doc)

    logger.info(
        f"[LOADER] Successfully loaded {len(documents)}/{len(supported_files)} files"
    )

    return documents