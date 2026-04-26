"""
Simple script to run the Flask application with better error handling
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app

    print("=" * 50)
    print("🚀 Azure Event Hub Web Application")
    print("=" * 50)
    print()
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
    print(f"   {str(e)}")
    print()
    print("Please install dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    print("Troubleshooting:")
    print("1. Ensure .env file is created with correct credentials")
    print("2. Check Azure Event Hub connection string and name")
    print("3. Verify all dependencies are installed")
    sys.exit(1)
