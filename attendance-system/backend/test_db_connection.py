import asyncio
import asyncpg
from db.base import engine, DATABASE_URL
from dotenv import load_dotenv
import os

load_dotenv()

async def test_direct_connection():
    """Test direct connection to Supabase (IPv6)."""
    try:
        user = "postgres"
        password = os.getenv("password")
        host = "db.uyuaukappnndpajjvvsi.supabase.co"
        port = 5432
        dbname = "postgres"
        
        print(f"Testing DIRECT connection to {host}:{port}")
        
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=dbname,
            host=host,
            port=port,
            ssl='require'
        )
        
        result = await conn.fetchval('SELECT version();')
        print(f"✅ Direct connection successful!")
        print(f"PostgreSQL version: {result[:50]}...")
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Direct connection failed: {e}")
        return False

async def test_transaction_pooler():
    """Test transaction pooler connection (IPv4 compatible)."""
    try:
        user = "postgres.uyuaukappnndpajjvvsi"
        password = os.getenv("password")
        host = "aws-0-ap-south-1.pooler.supabase.com"
        port = 6543
        dbname = "postgres"
        
        print(f"Testing TRANSACTION POOLER connection to {host}:{port}")
        
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=dbname,
            host=host,
            port=port,
            ssl='require'
        )
        
        result = await conn.fetchval('SELECT version();')
        print(f"✅ Transaction pooler connection successful!")
        print(f"PostgreSQL version: {result[:50]}...")
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Transaction pooler connection failed: {e}")
        return False

async def test_session_pooler():
    """Test session pooler connection (IPv4 compatible)."""
    try:
        user = "postgres.uyuaukappnndpajjvvsi"
        password = os.getenv("password")
        host = "aws-0-ap-south-1.pooler.supabase.com"
        port = 5432
        dbname = "postgres"
        
        print(f"Testing SESSION POOLER connection to {host}:{port}")
        
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=dbname,
            host=host,
            port=port,
            ssl='require'
        )
        
        result = await conn.fetchval('SELECT version();')
        print(f"✅ Session pooler connection successful!")
        print(f"PostgreSQL version: {result[:50]}...")
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Session pooler connection failed: {e}")
        return False

async def test_current_sqlalchemy_config():
    """Test the current SQLAlchemy configuration."""
    try:
        print(f"Testing CURRENT SQLALCHEMY config...")
        print(f"Connection method: {os.getenv('CONNECTION_METHOD', 'transaction_pooler')}")
        
        async with engine.connect() as connection:
            result = await connection.execute("SELECT version();")
            version = result.scalar()
            print(f"✅ SQLAlchemy connection successful!")
            print(f"PostgreSQL version: {version[:50]}...")
            return True
            
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

def check_network_type():
    """Check if we're on IPv4 or IPv6 network."""
    import socket
    
    print("Checking network connectivity type...")
    
    # Test IPv6
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("ipv6.google.com", 80))
        sock.close()
        print("✅ IPv6 connectivity available")
        ipv6_available = True
    except:
        print("❌ IPv6 connectivity not available")
        ipv6_available = False
    
    # Test IPv4
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("8.8.8.8", 53))
        sock.close()
        print("✅ IPv4 connectivity available")
        ipv4_available = True
    except:
        print("❌ IPv4 connectivity not available")
        ipv4_available = False
    
    return ipv4_available, ipv6_available

async def main():
    """Run all Supabase connection tests."""
    print("=" * 60)
    print("SUPABASE CONNECTION TESTING - ALL METHODS")
    print("=" * 60)
    
    # Check network type
    ipv4, ipv6 = check_network_type()
    print()
    
    # Test all connection methods
    methods_tested = 0
    successful_methods = []
    
    if ipv6:
        print("Testing Direct Connection (IPv6)...")
        if await test_direct_connection():
            successful_methods.append("Direct Connection (IPv6)")
        methods_tested += 1
        print()
    
    print("Testing Transaction Pooler (IPv4)...")
    if await test_transaction_pooler():
        successful_methods.append("Transaction Pooler (IPv4)")
    methods_tested += 1
    print()
    
    print("Testing Session Pooler (IPv4)...")
    if await test_session_pooler():
        successful_methods.append("Session Pooler (IPv4)")
    methods_tested += 1
    print()
    
    # Test current SQLAlchemy config
    print("Testing Current SQLAlchemy Configuration...")
    if await test_current_sqlalchemy_config():
        successful_methods.append("Current SQLAlchemy Config")
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Methods tested: {methods_tested}")
    print(f"Successful connections: {len(successful_methods)}")
    
    if successful_methods:
        print("✅ Working connection methods:")
        for method in successful_methods:
            print(f"   - {method}")
        
        if "Current SQLAlchemy Config" in successful_methods:
            print("\n🎉 Your current configuration is working!")
        else:
            print("\n💡 Recommendation: Update your .env file to use one of the working methods")
            
            if "Transaction Pooler (IPv4)" in successful_methods:
                print("   Set CONNECTION_METHOD=transaction_pooler in your .env file")
            elif "Session Pooler (IPv4)" in successful_methods:
                print("   Set CONNECTION_METHOD=session_pooler in your .env file")
            elif "Direct Connection (IPv6)" in successful_methods:
                print("   Set CONNECTION_METHOD=direct in your .env file")
    else:
        print("❌ No connection methods worked. Please check:")
        print("   1. Your password is correct")
        print("   2. Your Supabase project is not paused")
        print("   3. Your network allows database connections")

if __name__ == "__main__":
    asyncio.run(main())