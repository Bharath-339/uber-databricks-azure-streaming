# 📋 Web Application Summary

## What Has Been Created

I've created a complete web application in the `webapp` folder that allows you to send events to Azure Event Hub. Here's what you have:

### Core Files

| File | Purpose |
|------|---------|
| **app.py** | Main Flask application with routes for sending events |
| **config.py** | Configuration management for Azure Event Hub credentials |
| **run.py** | Easy-to-use script to start the application |
| **requirements.txt** | Python dependencies list |
| **.env.example** | Template for environment configuration |

### Frontend

| File | Purpose |
|------|---------|
| **templates/index.html** | Beautiful web UI for sending events |

### Setup Scripts

| File | Purpose |
|------|---------|
| **setup.sh** | Quick setup script for macOS/Linux |
| **setup.bat** | Quick setup script for Windows |

### Documentation

| File | Purpose |
|------|---------|
| **README.md** | Comprehensive documentation |

## Getting Started (Quick Steps)

### 1. Setup (Choose one for your OS)

**Windows:**
```bash
cd webapp
setup.bat
```

**macOS/Linux:**
```bash
cd webapp
bash setup.sh
```

### 2. Configure Credentials

Edit the `.env` file with your Azure Event Hub credentials:
```
EVENT_HUB_CONNECTION_STRING=your_connection_string_here
EVENT_HUB_NAME=your_event_hub_name_here
```

### 3. Run the Application

```bash
python run.py
```

Or directly:
```bash
python app.py
```

### 4. Access the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

## Features

✅ **Web User Interface** - Clean, modern dashboard to send events
✅ **REST API** - Programmatic access to send events
✅ **Custom Data Support** - Send additional JSON data with messages
✅ **Error Handling** - Comprehensive error messages
✅ **Health Check** - Built-in health check endpoint
✅ **Event Preview** - See event details before sending
✅ **Responsive Design** - Works on desktop and mobile

## API Endpoints

### Send Event
```
POST /send-event
```
Request:
```json
{
  "message": "Your event message",
  "data": {
    "key": "value"
  }
}
```

### Health Check
```
GET /health
```

## File Structure

```
webapp/
├── app.py                          # Main Flask app
├── config.py                       # Configuration
├── run.py                          # Easy run script
├── requirements.txt                # Dependencies
├── .env.example                    # Env template
├── setup.sh                        # Setup script (Unix)
├── setup.bat                       # Setup script (Windows)
├── README.md                       # Full documentation
├── QUICKSTART.md                   # This file
└── templates/
    └── index.html                  # Web UI
```

## Next Steps

1. ✅ Get your Azure Event Hub credentials from Azure Portal
2. ✅ Run setup script for your OS
3. ✅ Update `.env` with your credentials
4. ✅ Run the application
5. ✅ Start sending events!

## Troubleshooting

### Connection Error
- Verify credentials in `.env` file
- Check Azure Event Hub namespace is active
- Ensure firewall allows outbound connections

### Module Not Found
```bash
pip install -r requirements.txt
```

### Port Already in Use
The app runs on port 5000. If busy, edit `app.py` or `run.py`:
```python
app.run(port=5001)  # Change to different port
```

## Support Files

All files include:
- ✅ Type hints and documentation
- ✅ Error handling and validation
- ✅ Comments and explanations
- ✅ Professional structure and best practices

Enjoy your Azure Event Hub integration! 🚀
