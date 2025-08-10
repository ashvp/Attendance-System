import asyncio
from db.base import engine, DATABASE_URL, test_connection

async def main():
    """Test the new database configuration."""
    print("=" * 50)
    print("TESTING NEW DATABASE CONFIGURATION")
    print("=" * 50)
    
    print("Testing database connection...")
    success = await test_connection()
    
    if success:
        print("\n🎉 Configuration is working!")
        print("You can now run:")
        print("  alembic revision --autogenerate -m 'Initial database schema'")
    else:
        print("\n❌ Configuration needs adjustment.")
        print("Check your .env file and connection method.")
    
    # Clean up
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())