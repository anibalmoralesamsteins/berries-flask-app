# data_processor.py
import statistics
import json
import matplotlib.pyplot as plt
import os

def process_berry_data(results):
    """Process the data from the API and return the statistics of the growth time of all berries."""
    result_data = {
        "berries_names": [],
        "min_growth_time": float('inf'),
        "max_growth_time": float('-inf'),
    }

    growth_times = []
    min_berry = ""
    max_berry = ""
    
    # Extract the data from the results
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

    # Return the statistics as a JSON string
    return json.dumps({
        "berries_names": result_data["berries_names"],
        "min_growth_time": f"The minimum growth time is {result_data['min_growth_time']} hours. It belongs to the {min_berry} berry.",
        "median_growth_time": f"The median growth time is {result_data['median_growth_time']} hours.",
        "max_growth_time": f"The maximum growth time is {result_data['max_growth_time']} hours. It belongs to the {max_berry} berry.",
        "variance_growth_time": f"The variance of the growth time is {result_data['variance_growth_time']}.",
        "mean_growth_time": f"The mean growth time of all berries is {result_data['mean_growth_time']} hours.",
        "frequency_growth_time": f"The frequency of growth time is {result_data['frequency_growth_time']}."
    })
