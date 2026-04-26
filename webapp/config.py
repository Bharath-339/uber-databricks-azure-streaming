import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Event Hub Configuration
EVENT_HUB_CONNECTION_STRING = os.getenv('EVENT_HUB_CONNECTION_STRING')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')

# Validate required configuration
if not EVENT_HUB_CONNECTION_STRING:
    raise ValueError(
        "Missing required environment variable: EVENT_HUB_CONNECTION_STRING\n"
        "Please check your .env file and ensure EVENT_HUB_CONNECTION_STRING is set correctly.\n"
        "Format: Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=..."
    )

if not EVENT_HUB_NAME:
    raise ValueError(
        "Missing required environment variable: EVENT_HUB_NAME\n"
        "Please check your .env file and ensure EVENT_HUB_NAME is set correctly.\n"
        "Example: my-event-hub"
    )
