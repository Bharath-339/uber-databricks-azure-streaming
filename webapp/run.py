"""
Simple script to run the Flask application with better error handling
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_prerequisites():
    """Check if all required configuration files and variables exist"""
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Error: .env file not found")
        print()
        print("To set up the application:")
        print("1. Copy .env.example to .env")
        print("2. Add your Azure Event Hub credentials:")
        print("   - EVENT_HUB_CONNECTION_STRING")
        print("   - EVENT_HUB_NAME")
        print()
        print("Commands:")
        print("   copy .env.example .env  (Windows)")
        print("   cp .env.example .env    (macOS/Linux)")
        sys.exit(1)

    # Check if environment variables are set
    with open('.env', 'r') as f:
        env_content = f.read()
        if 'your_connection_string_here' in env_content or 'your_event_hub_name_here' in env_content:
            print("❌ Error: .env file contains placeholder values")
            print()
            print("Please update .env with your actual Azure Event Hub credentials:")
            print("   EVENT_HUB_CONNECTION_STRING=Endpoint=sb://...")
            print("   EVENT_HUB_NAME=your-event-hub-name")
            sys.exit(1)

try:
    # Check prerequisites first
    check_prerequisites()

    # Import Flask app
    from app import app

    print("=" * 50)
    print("🚀 Uber Event Hub Web Application")
    print("=" * 50)
    print()
    print("✓ Configuration loaded successfully")
    print("✓ Starting server...")
    print()
    print("📱 Web Interface: http://localhost:5000")
    print("🔧 API Endpoint: http://localhost:5000/send-event")
    print("💓 Health Check: http://localhost:5000/health")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    print()

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

except ImportError as e:
    print("❌ Error: Missing required dependencies")
    print(f"   Details: {str(e)}")
    print()
    print("Please install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("If issues persist, try reinstalling:")
    print("   pip install --upgrade -r requirements.txt")
    sys.exit(1)

except ValueError as e:
    print("❌ Error: Configuration error")
    print(f"   {str(e)}")
    print()
    print("Please check your .env file and ensure all required variables are set")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    print("Troubleshooting:")
    print("1. Ensure .env file is created with correct credentials")
    print("2. Check Azure Event Hub connection string and name")
    print("3. Verify all dependencies are installed: pip install -r requirements.txt")
    print("4. Check that the connection string format is correct")
    sys.exit(1)
