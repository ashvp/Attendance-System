import socket
import subprocess
import platform
import os
from dotenv import load_dotenv

load_dotenv()

def test_dns_resolution():
    """Test DNS resolution for the Supabase host."""
    host = os.getenv("host")
    print(f"Testing DNS resolution for: {host}")
    
    try:
        # Get IP address
        ip = socket.gethostbyname(host)
        print(f"✅ DNS Resolution successful: {host} → {ip}")
        return ip
    except socket.gaierror as e:
        print(f"❌ DNS Resolution failed: {e}")
        return None

def test_internet_connectivity():
    """Test basic internet connectivity."""
    print("Testing basic internet connectivity...")
    
    # Test with multiple reliable hosts
    test_hosts = [
        "8.8.8.8",      # Google DNS
        "1.1.1.1",      # Cloudflare DNS
        "google.com",   # Google
    ]
    
    for host in test_hosts:
        try:
            socket.create_connection((host, 80 if host != "google.com" else 443), timeout=5)
            print(f"✅ Can reach {host}")
            return True
        except Exception as e:
            print(f"❌ Cannot reach {host}: {e}")
            continue
    
    return False

def test_dns_servers():
    """Test DNS server configuration."""
    print("\nChecking DNS servers...")
    
    system = platform.system().lower()
    
    if system == "linux":
        try:
            with open('/etc/resolv.conf', 'r') as f:
                content = f.read()
                print("Current DNS configuration (/etc/resolv.conf):")
                print(content)
        except Exception as e:
            print(f"Could not read DNS config: {e}")
    
    # Test with different DNS servers
    dns_servers = ["8.8.8.8", "1.1.1.1", "8.8.4.4"]
    host = os.getenv("host")
    
    for dns in dns_servers:
        try:
            print(f"Testing with DNS server {dns}...")
            # This is a simplified test - in practice, you'd need dnspython for proper DNS testing
            result = subprocess.run(
                ["nslookup", host, dns], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ {dns} can resolve {host}")
                return True
            else:
                print(f"❌ {dns} failed to resolve {host}")
        except Exception as e:
            print(f"❌ Error testing DNS {dns}: {e}")
    
    return False

def test_ping():
    """Test ping to the Supabase host."""
    host = os.getenv("host")
    print(f"\nTesting ping to {host}...")
    
    system = platform.system().lower()
    ping_cmd = ["ping", "-c", "4"] if system != "windows" else ["ping", "-n", "4"]
    ping_cmd.append(host)
    
    try:
        result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Ping successful")
            print("Sample output:", result.stdout.split('\n')[0])
            return True
        else:
            print("❌ Ping failed")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Ping test failed: {e}")
        return False

def suggest_fixes():
    """Suggest potential fixes based on the diagnosis."""
    print("\n" + "="*50)
    print("SUGGESTED FIXES:")
    print("="*50)
    
    print("1. 🌐 Check your internet connection:")
    print("   - Try browsing to https://supabase.com")
    print("   - Restart your network connection")
    
    print("\n2. 🔧 Try different DNS servers:")
    print("   - Temporarily use Google DNS: 8.8.8.8, 8.8.4.4")
    print("   - Or Cloudflare DNS: 1.1.1.1, 1.0.0.1")
    
    if platform.system().lower() == "linux":
        print("\n   On Linux (temporary):")
        print("   sudo nano /etc/resolv.conf")
        print("   Add these lines:")
        print("   nameserver 8.8.8.8")
        print("   nameserver 8.8.4.4")
    
    print("\n3. 🔒 Check firewall/proxy settings:")
    print("   - Corporate firewall might block PostgreSQL port 5432")
    print("   - Try from a different network (mobile hotspot)")
    
    print("\n4. 📋 Verify Supabase project status:")
    print("   - Log into your Supabase dashboard")
    print("   - Check if your project is paused or has issues")
    print("   - Verify the connection string in Settings → Database")
    
    print("\n5. 🔄 Try alternative connection methods:")
    print("   - Use Supabase connection pooler (port 6543)")
    print("   - Try connecting via Supabase API instead")

def main():
    print("="*60)
    print("SUPABASE DNS & CONNECTIVITY DIAGNOSTICS")
    print("="*60)
    
    print(f"Target host: {os.getenv('host')}")
    print(f"Target port: {os.getenv('port')}")
    print()
    
    # Run diagnostic tests
    internet_ok = test_internet_connectivity()
    print()
    
    if internet_ok:
        dns_ok = test_dns_resolution()
        print()
        
        if not dns_ok:
            dns_servers_ok = test_dns_servers()
            ping_ok = test_ping()
        else:
            # If DNS works, test ping
            ping_ok = test_ping()
    
    suggest_fixes()

if __name__ == "__main__":
    main()