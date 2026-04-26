from flask import Flask, render_template, request, jsonify
from azure.eventhub import EventHubProducerClient, EventData
from config import EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME
from data import generate_uber_ride_confirmation
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
    API endpoint to send Uber ride events to Azure Event Hub
    Expected JSON payload: {"count": number_of_events_to_generate}
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        count = data.get('count', 1)

        # Validate count
        if not isinstance(count, int) or count < 1 or count > 100:
            return jsonify({'error': 'Count must be between 1 and 100'}), 400

        # Generate Uber ride data and send to Event Hub
        producer_client = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STRING,
            eventhub_name=EVENT_HUB_NAME
        )

        batch = producer_client.create_batch()
        events_added = 0

        # Generate and add events to batch
        for _ in range(count):
            # Generate Uber ride data
            ride_data = generate_uber_ride_confirmation()

            # Add event to batch
            batch.add(EventData(json.dumps(ride_data)))
            events_added += 1

        # Send the batch
        producer_client.send_batch(batch)
        producer_client.close()

        logger.info(f"Successfully sent {events_added} event(s) to Event Hub")

        return jsonify({
            'success': True,
            'message': f'{events_added} event(s) sent successfully',
            'events_sent': events_added,
            'timestamp': str(datetime.now())
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
