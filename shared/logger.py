# ============================================
# shared/logger.py
# Central Logger for entire project
# ============================================

import sys
import os
from loguru import logger

# Remove default loguru logger
logger.remove()

# Create logs folder if not exists
os.makedirs("./logs", exist_ok=True)

# ----------------------------
# Console Logger - Simple format, no conflict
# ----------------------------
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
    colorize=False
)

# ----------------------------
# File Logger - Saves to logs/app.log
# ----------------------------
logger.add(
    "./logs/app.log",
    level="DEBUG",
    rotation="10 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}"
)


# ----------------------------
# Helper functions
# ----------------------------

def log_agent_start(agent_name: str, query: str):
    logger.info(f"[{agent_name.upper()}] Started | Query: {query[:50]}")


def log_agent_end(agent_name: str, status: str = "success"):
    logger.info(f"[{agent_name.upper()}] Finished | Status: {status}")


def log_agent_error(agent_name: str, error: str):
    logger.error(f"[{agent_name.upper()}] ERROR | {error}")


def log_db_query(table: str, operation: str):
    logger.debug(f"[DATABASE] {operation} on table: {table}")


def log_mistral_call(model: str, tokens: int = 0):
    logger.debug(f"[MISTRAL] Called model: {model} | Tokens: {tokens}")


__all__ = [
    "logger",
    "log_agent_start",
    "log_agent_end",
    "log_agent_error",
    "log_db_query",
    "log_mistral_call"
]