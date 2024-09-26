import asyncpg
import os
from typing import Dict
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

def credentials() -> Dict[str, str]:
    """
    Retrieves database connection credentials from environment variables.

    Returns:
        Dict[str, str]: A dictionary containing database connection credentials.
    """
    creds = {
        'host': os.getenv("POSTGRES_HOST"),
        'database': os.getenv("POSTGRES_DATABASE"),
        'user': os.getenv("POSTGRES_USER"),
        'password': str(os.getenv("POSTGRES_PASSWORD")),
        'port': str(os.getenv("POSTGRES_PORT"))  # Ensure port is string for asyncpg.connect
    }

    # Log the credentials being used (excluding the password for security)
    logger.info(f"Connecting with credentials: host={creds['host']}, database={creds['database']}, user={creds['user']}, port={creds['port']}")
    
    return creds

async def connect_db() -> asyncpg.Connection:
    """
    Establishes a connection to a PostgreSQL database using asyncpg with credentials from environment variables.

    Returns:
        asyncpg.Connection: An asynchronous database connection object.
    
    Raises:
        asyncpg.PostgresError: If there's an error connecting to the database.
        KeyError: If any required key is missing in the credentials dictionary.
    """
    creds = credentials()
    required_keys = {'host', 'password', 'database', 'user', 'port'}
    
    if not required_keys.issubset(creds):
        missing_keys = required_keys - set(creds.keys())
        logger.error(f"Missing required keys: {', '.join(missing_keys)} in credentials dictionary")
        raise KeyError(f"Missing required keys: {', '.join(missing_keys)} in credentials dictionary")

    try:
        logger.info("Attempting to connect to the database...")
        conn = await asyncpg.connect(**creds)
        logger.info("Successfully connected to the database.")
        return conn
    except asyncpg.PostgresError as e:
        logger.error(f"Database connection error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise