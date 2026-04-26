from flask import Flask, render_template, request, jsonify
from azure.eventhub import EventHubProducerClient, EventData
from config import EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME
from datetime import datetime
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')


@app.route('/send-event', methods=['POST'])
def send_event():
    """
    API endpoint to send an event to Azure Event Hub
    Expected JSON payload: {"message": "your message", "data": {...}}
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        message = data.get('message', 'No message provided')
        custom_data = data.get('data', {})

        # Prepare the event payload
        event_payload = {
            'message': message,
            'data': custom_data,
            'timestamp': str(datetime.now())
        }

        # Send to Azure Event Hub
        producer_client = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STRING,
            eventhub_name=EVENT_HUB_NAME
        )

        batch = producer_client.create_batch()
        batch.add(EventData(json.dumps(event_payload)))

        producer_client.send_batch(batch)
        producer_client.close()

        logger.info(f"Event sent successfully: {event_payload}")

        return jsonify({
            'success': True,
            'message': 'Event sent successfully',
            'event': event_payload
        }), 200

    except Exception as e:
        logger.error(f"Error sending event: {str(e)}")
        return jsonify({
            'error': f'Failed to send event: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
