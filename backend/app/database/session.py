"""
Database connection, session management, and intelligent fallback handler.
Primary target: MySQL 8.0+ via PyMySQL.
Fallback target: SQLite (sqlite:///./app.db) for immediate zero-config execution.
"""

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("database")

Base = declarative_base()

DEFAULT_MYSQL_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/code_review_db"
)
FALLBACK_SQLITE_URL = "sqlite:///./app.db"

def init_engine():
    """Attempt connecting to MySQL; seamlessly fall back to SQLite if offline."""
    url = os.getenv("DATABASE_URL", DEFAULT_MYSQL_URL)
    is_sqlite = url.startswith("sqlite")

    if not is_sqlite:
        try:
            # Short timeout to test MySQL availability
            test_engine = create_engine(
                url,
                connect_args={"connect_timeout": 3},
                pool_pre_ping=True
            )
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("[Database] Connected successfully to primary MySQL database.")
            return test_engine, "MySQL"
        except Exception as err:
            logger.warning(
                f"[Database] Primary MySQL connection failed ({err}). "
                f"Falling back to local SQLite ({FALLBACK_SQLITE_URL}) for zero-config local execution."
            )

    # SQLite fallback
    sqlite_engine = create_engine(
        FALLBACK_SQLITE_URL,
        connect_args={"check_same_thread": False}
    )
    return sqlite_engine, "SQLite"

engine, ACTIVE_DB_TYPE = init_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI dependency yielding database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all ORM-mapped tables and ensure column migrations."""
    # Ensure all models are registered with Base metadata
    import backend.app.models.entities  # noqa
    Base.metadata.create_all(bind=engine)

    # Safe schema migration for newly added columns
    try:
        with engine.begin() as conn:
            if ACTIVE_DB_TYPE == "SQLite":
                res = conn.execute(text("PRAGMA table_info(issues)"))
                existing_cols = {row[1] for row in res.fetchall()}
            else:
                res = conn.execute(text("DESCRIBE issues"))
                existing_cols = {row[0] for row in res.fetchall()}

            for col in ["software_defect", "bug_fix", "future_guidelines"]:
                if col not in existing_cols:
                    conn.execute(text(f"ALTER TABLE issues ADD COLUMN {col} TEXT"))
    except Exception as e:
        logger.warning(f"[Database] Migration check notice: {e}")

    logger.info(f"[Database] Schema initialized on active database: {ACTIVE_DB_TYPE}")

# Automatically create tables so database is immediately available
create_tables()
