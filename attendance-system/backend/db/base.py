from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create declarative base
Base = declarative_base()

def get_database_url():
    """Get the appropriate database URL based on connection method."""
    
    password = os.getenv("password")
    connection_method = os.getenv("CONNECTION_METHOD", "session_pooler")
    
    if connection_method == "session_pooler":
        # Use session pooler (IPv4) - RECOMMENDED based on your test
        user = "postgres.uyuaukappnndpajjvvsi"
        host = "aws-0-ap-south-1.pooler.supabase.com"
        port = 5432
        dbname = "postgres"
        
    elif connection_method == "transaction_pooler":
        # Use transaction pooler (IPv4)
        user = "postgres.uyuaukappnndpajjvvsi"
        host = "aws-0-ap-south-1.pooler.supabase.com"
        port = 6543
        dbname = "postgres"
        
    elif connection_method == "direct":
        # Direct connection (IPv6) - fallback to env vars if available
        user = os.getenv("user", "postgres")
        host = os.getenv("host", "db.uyuaukappnndpajjvvsi.supabase.co")
        port = int(os.getenv("port", 5432))
        dbname = os.getenv("dbname", "postgres")
        
    elif connection_method == "env_vars":
        # Use environment variables (your original approach)
        user = os.getenv("user")
        host = os.getenv("host")
        port = int(os.getenv("port", 5432))
        dbname = os.getenv("dbname")
        
        if not all([user, host, dbname]):
            raise ValueError("Missing required environment variables: user, host, dbname")
    
    else:
        raise ValueError(f"Unknown connection method: {connection_method}")
    
    # Construct the DATABASE_URL
    DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
    return DATABASE_URL

def create_database_engine():
    """Create the SQLAlchemy async engine with proper configuration."""
    
    DATABASE_URL = get_database_url()
    connection_method = os.getenv("CONNECTION_METHOD", "session_pooler")
    
    # Base connect_args for SSL
    connect_args = {
        "ssl": "require"  # Use "ssl" instead of "sslmode" for asyncpg
    }
    
    # Add statement cache size for transaction pooler
    if connection_method == "transaction_pooler":
        connect_args["statement_cache_size"] = 0
    
    # Create async engine
    engine = create_async_engine(
        DATABASE_URL,
        connect_args=connect_args,
        echo=False,  # Set to True for SQL debugging
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    
    return engine, DATABASE_URL

# Create the engine and DATABASE_URL
engine, DATABASE_URL = create_database_engine()

# Test the connection (async version)
async def test_connection():
    """Test the database connection."""
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# Print configuration info
print(f"Database engine created with connection method: {os.getenv('CONNECTION_METHOD', 'session_pooler')}")
# Hide password in URL for security
safe_url = DATABASE_URL.replace(os.getenv('password', 'PASSWORD'), '***')
print(f"Database URL: {safe_url}")