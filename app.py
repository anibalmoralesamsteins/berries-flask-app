from flask import Flask, Response
from api_client import fetch_all_berries
from data_processor import process_berry_data
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/allBerryStats', methods=['GET'])
def all_berry_stats():
    """Get the statistics of the growth time of all berries from the PokeAPI."""
    # Create a response object
    res = Response()
    res.status = 200
    res.content_type = os.getenv('RESPONSE_CONTENT_TYPE', '')

    try:
        # Get API URL and handle missing environment variable
        poke_api_url = os.getenv('POKE_API_URL')
        if not poke_api_url:
            return "POKE_API_URL environment variable is not set", 500
        
        # Fetch the berry data
        results = fetch_all_berries(poke_api_url)
        
        # Process the data
        res.response = process_berry_data(results)
        return res

    except Exception as e:
        res.status, res.response = 500, json.dumps({'error': str(e)})
        return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
