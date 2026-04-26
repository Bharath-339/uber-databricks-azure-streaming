import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Event Hub Configuration
EVENT_HUB_CONNECTION_STRING = os.getenv('EVENT_HUB_CONNECTION_STRING')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')

# Validate required configuration
if not EVENT_HUB_CONNECTION_STRING or not EVENT_HUB_NAME:
    raise ValueError(
        "Missing required environment variables. "
        "Please ensure EVENT_HUB_CONNECTION_STRING and EVENT_HUB_NAME are set."
    )
