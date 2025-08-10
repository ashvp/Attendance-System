import asyncio
from sqlalchemy import text
from db.base import Base, engine
import logging

# Import all your existing models
from db.models.user import User
from db.models.account import Account
from db.models.attendance import Attendance
from db.models.student_profile import StudentProfile

logger = logging.getLogger(__name__)

async def get_existing_tables() -> list:
    """Get list of all existing tables in the database."""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result.fetchall()]
            return tables
    except Exception as e:
        logger.error(f"Error getting existing tables: {e}")
        return []

async def create_tables_if_not_exist():
    """Create all tables defined in your models if they don't exist."""
    try:
        print("🔍 Checking database connection...")
        
        # Test database connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"📡 Connected to: {version[:50]}...")
        
        # Get existing tables
        existing_tables = await get_existing_tables()
        print(f"📋 Existing tables: {existing_tables}")
        
        # Expected tables from your models
        expected_tables = ['accounts', 'users', 'student_profiles', 'attendance']
        missing_tables = [table for table in expected_tables if table not in existing_tables]
        
        if not missing_tables:
            print("✅ All tables already exist!")
            return True
        
        print(f"🔨 Creating missing tables: {missing_tables}")
        
        # Create all tables (SQLAlchemy will only create missing ones)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Verify tables were created
        final_tables = await get_existing_tables()
        print(f"📋 Final tables: {final_tables}")
        print("✅ Tables created successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        logger.error(f"Table creation error: {e}")
        return False

# For running standalone
async def main():
    await create_tables_if_not_exist()

if __name__ == "__main__":
    asyncio.run(main())