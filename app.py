from requests import get
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import statistics
import flask
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = flask.Flask(__name__)

# Define a simple GET endpoint
def process_berry_data(results):
    """"Process the data from the API and return the statistics of the growth time of all berries.

    Args:
        results (list): The list of berries from the API.

    Returns:
        dict: The statistics of the growth time of all berries.
    """
    # Initialize the result data
    result_data = {
        "berries_names": [],
        "min_growth_time": float('inf'),
        "max_growth_time": float('-inf'),
    }

    # Extract the data from the results
    growth_times = []
    min_berry = ""
    max_berry = ""
    for berry in results:
        result_data["berries_names"].append(berry["name"])
        if berry["growth_time"] < result_data["min_growth_time"]:
            result_data["min_growth_time"] = berry["growth_time"]
            min_berry = berry["name"]
        if berry["growth_time"] > result_data["max_growth_time"]:
            result_data["max_growth_time"] = berry["growth_time"]
            max_berry = berry["name"]
        growth_times.append(berry["growth_time"])

    # Calculate statistics
    result_data["median_growth_time"] = statistics.median(growth_times)
    result_data["variance_growth_time"] = statistics.variance(growth_times)
    result_data["mean_growth_time"] = statistics.mean(growth_times)
    result_data["frequency_growth_time"] = len(growth_times)

    # Generate the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(growth_times, bins=10, edgecolor='black', color='skyblue')
    plt.title('Berry Growth Time Distribution')
    plt.xlabel('Growth Time (hours)')
    plt.ylabel('Frequency')

    # Create a directory if it does not exist
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')

    # Save the histogram image to a file
    histogram_image_path = './tmp/berry_growth_histogram.png'
    plt.savefig(histogram_image_path)
    plt.close()  # Close the plot to release memory

    return json.dumps({
        "berries_names": result_data["berries_names"],
        "min_growth_time": f"The minimum growth time is {result_data['min_growth_time']} hours. It belongs to the {min_berry} berry.",
        "median_growth_time": f"The median growth time is {result_data['median_growth_time']} hours.",
        "max_growth_time": f"The maximum growth time is {result_data['max_growth_time']} hours. It belongs to the {max_berry} berry.",
        "variance_growth_time": f"The variance of the growth time is {result_data['variance_growth_time']}.",
        "mean_growth_time": f"The mean growth time of all berries is {result_data['mean_growth_time']} hours.",
        "frequency_growth_time": f"The frequency of growth time is {result_data['frequency_growth_time']}."
    })

# Define a simple GET endpoint
@app.route('/allBerryStats', methods=['GET'])
def all_berry_stats():
    """Get the statistics of the growth time of all berries from the PokeAPI.

    Returns:
        flask.Response: The response object with the statistics of the growth time of all berries.
    """
    # Check if Testing
    test_env = os.getenv('TEST_ENV', 'False') == 'True'
    # Create a response object
    res = flask.Response()
    res.status = 200
    res.content_type = os.getenv('RESPONSE_CONTENT_TYPE', '')
    try:
        if test_env:

            # open url_response.json file as dict
            with open('./mock_responses/berries_response.json') as f:
                results = json.load(f)
                
            # Process the data
            res.response = process_berry_data(results)
            return res

        else:
            # Handle missing environment variable
            if not os.getenv('POKE_API_URL'):
                return "POKE_API_URL environment variable is not set", 500

            # Get the data from the API
            response = get(f"{os.getenv('POKE_API_URL')}/berry")

            # Handle the response
            if response.ok:

                # Parse the JSON response
                data = response.json()
                url_results = data["results"]

                # Handle pagination
                while data["next"] is not None:
                    response = get(data["next"])
                    if response.ok:
                        data = response.json()
                        url_results.extend(data["results"])
                    else:
                        # Return response with error status code
                        res.status, res.response = response.status_code, response.content
                        return res
                
                # Request the data of each berry
                results = []
                for url_result in url_results:
                    response = get(url_result["url"])
                    if response.ok:
                        results.append(response.json())
                    else:
                        # Return response with error status code
                        res.status, res.response = response.status_code, response.content
                        return res
                
                # Process the data
                res.response = process_berry_data(results)

                return res
        
            else:
                # Return response with error status code
                res.status, res.response = response.status_code, response.content
                return res
    except Exception as e:
        # Return server error status code
        res.status, res.response = 500, json.dumps({'error':str(e)})
        return res

# Start the Flask app, making it accessible externally (0.0.0.0)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)