# Azure Event Hub Web Application

A simple Flask web application to send events to Azure Event Hub.

## Features

- **Web UI**: Clean, modern interface for sending events
- **Event Hub Integration**: Direct integration with Azure Event Hub
- **JSON Support**: Send custom JSON data along with messages
- **API Endpoint**: RESTful API for programmatic event sending
- **Error Handling**: Comprehensive error messages and validation
- **Health Check**: Built-in health check endpoint

## Prerequisites

- Python 3.8+
- Azure Event Hub instance
- Connection string and Event Hub name from Azure Portal

## Installation

1. **Navigate to the webapp directory:**
   ```bash
   cd webapp
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Azure Event Hub credentials:
     ```
     EVENT_HUB_CONNECTION_STRING=your_connection_string
     EVENT_HUB_NAME=your_event_hub_name
     ```

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter your event message
3. Optionally add custom JSON data
4. Click "Send Event"
5. View the event preview and confirmation

### API Usage

**Endpoint:** `POST /send-event`

**Request Example:**
```bash
curl -X POST http://localhost:5000/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello Event Hub",
    "data": {
      "user_id": "123",
      "action": "purchase",
      "amount": 99.99
    }
  }'
```

**Success Response:**
```json
{
  "success": true,
  "message": "Event sent successfully",
  "event": {
    "message": "Hello Event Hub",
    "data": {
      "user_id": "123",
      "action": "purchase",
      "amount": 99.99
    },
    "timestamp": "2024-01-15 10:30:45.123456"
  }
}
```

**Error Response:**
```json
{
  "error": "Failed to send event: Connection error"
}
```

### Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy"
}
```

## Project Structure

```
webapp/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment configuration
├── templates/
│   └── index.html         # Web UI template
└── README.md              # This file
```

## Configuration Details

### Getting Azure Event Hub Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Event Hub Namespace
3. Go to "Shared access policies" → "RootManageSharedAccessKey"
4. Copy the "Connection string–primary key"
5. Your Event Hub name is shown in the namespace overview

### Environment Variables

- `EVENT_HUB_CONNECTION_STRING`: Full connection string from Azure Portal
- `EVENT_HUB_NAME`: Name of your Event Hub instance

## Development

### Adding Custom Routes

Edit `app.py` to add new Flask routes:

```python
@app.route('/api/custom', methods=['GET', 'POST'])
def custom_route():
    return jsonify({'status': 'ok'})
```

### Modifying the UI

Edit `templates/index.html` to customize the web interface.

## Troubleshooting

### Connection Error
- Verify `EVENT_HUB_CONNECTION_STRING` is correct
- Check Azure Event Hub namespace is active
- Ensure your IP is not blocked by firewall rules

### Invalid JSON in Custom Data
- Ensure the custom data field contains valid JSON format
- Use double quotes for strings: `{"key": "value"}`

### Module Not Found Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check you're using the correct Python environment

## Dependencies

- **Flask**: Web framework
- **azure-eventhub**: Azure Event Hub SDK for Python
- **python-dotenv**: Environment variable management

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the Azure Event Hub documentation
2. Review error messages in the console logs
3. Verify Azure credentials and network connectivity
