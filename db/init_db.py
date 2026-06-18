# Database Initializer
# Run this ONCE to set up entire database
# Creates all tables + fills sample data

from db.session import create_all_tables, test_connection
from db.seed_data import run_all_seeds
from shared.logger import logger


def initialize_database():
    """
    Complete database setup in 3 steps:
    Step 1 - Test MySQL connection
    Step 2 - Create all tables
    Step 3 - Fill sample data
    """

    logger.info("=" * 50)
    logger.info("[INIT] Starting database initialization...")
    logger.info("=" * 50)

    # Step 1 - Test connection
    logger.info("[INIT] Step 1: Testing MySQL connection...")
    if not test_connection():
        logger.error("[INIT] Cannot connect to MySQL. Check your .env settings.")
        return False

    # Step 2 - Create tables
    logger.info("[INIT] Step 2: Creating database tables...")
    create_all_tables()

    # Step 3 - Seed data
    logger.info("[INIT] Step 3: Seeding sample data...")
    run_all_seeds()

    logger.info("=" * 50)
    logger.info("[INIT] Database initialization COMPLETE!")
    logger.info("[INIT] Tables created: departments, employees,")
    logger.info("[INIT]   users, leave_balances, leave_requests, audit_logs")
    logger.info("[INIT] Sample data: 5 departments, 10 employees, 10 users")
    logger.info("=" * 50)
    return True


if __name__ == "__main__":
    initialize_database()