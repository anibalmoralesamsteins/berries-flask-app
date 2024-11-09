# Berries Flask App

This project is a Flask web application that fetches data about berries from the [PokeAPI](https://pokeapi.co/), processes the data to calculate statistics (mean, median, variance, min, max), and generates a histogram of the berry growth times. The app exposes a RESTful API that returns berry data along with a histogram image showing the distribution of growth times.

## Features

- Fetches berry data from the PokeAPI.
- Calculates statistics for berry growth times (min, max, mean, median, variance).
- Generates a histogram graph of berry growth time distribution.
- Exposes a REST API endpoint to serve the processed data and the histogram image.

## Demo

You can view the live demo of the app running on a local server by following the instructions below.

### Example API Response:

When you make a GET request to `/allBerryStats`, the endpoint will return a JSON object with the statistics and a link to the histogram image. For example:

```json
{
  "berries_names": ["berry1", "berry2", "berry3"],
  "min_growth_time": "The minimum growth time is 5 hours. It belongs to the berry2 berry.",
  "max_growth_time": "The maximum growth time is 10 hours. It belongs to the berry1 berry.",
  "median_growth_time": "The median growth time is 7 hours.",
  "variance_growth_time": "The variance of the growth time is 5.0.",
  "mean_growth_time": "The mean growth time of all berries is 7.33 hours.",
  "frequency_growth_time": "The frequency of growth time is 3."
}
```
It will also create in the docker directory a tmp folder with the berry_growth_histogram png file for every growth time obtained.

## Installation

### Prerequisites

- **Docker** (Ensure Docker is installed on your system. You can download it from [here](https://www.docker.com/get-started)).

### Steps to Set Up Using Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anibalmoralesamsteins/berries-flask-app.git
   cd berries-flask-app
   ```
   
2. **Build the Docker image: From the project root directory (where the Dockerfile is located), run the following command to build the Docker image**:
    ```bash
    docker build -t berries-flask-app .
    ```

3. **Set up environment variables: Create a .env file in the root of the project (if it doesn't already exist) with the following content**:

     ```bash
    POKE_API_URL='https://pokeapi.co/api/v2'
    RESPONSE_CONTENT_TYPE='application/json'
     ```
4. **Run the Docker container: Once the image is built, you can run the application in a container with the following command**:

   ```bash
   docker run -p 5000:5000 berries-flask-app
   ```
    This command will start the Flask app and expose it on port 5000 of your local machine.

5. **Access the app using `curl`**:
   Once the Docker container is running, you can interact with the Flask API using `curl`, a command-line tool for making HTTP requests.

   To get the berry statistics along with the generated histogram, run the following `curl` command in your terminal:

   ```bash
   curl http://localhost:5000/allBerryStats
   ```

### Steps to Run using Virtual Environment

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/anibalmoralesamsteins/berries-flask-app.git
   cd berries-flask-app
   ```
   
2. **Set Up a Virtual Environment**

   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
     
3. **Install Dependencies**
   
   ```bash
   pip install -r requirements.txt
   ```
     
4. **Run the Flask App**
   
   ```bash
   flask run
   ```

The app should now be running on http://127.0.0.1:5000/.

## Running Tests

The project includes unit tests to verify the correct functioning of both the data processing and Flask routes.

### Steps to Run Tests

1. Ensure all dependencies are set up (**Virtual Environment installation** strongly recommended).
2. Run the tests by executing the following command:
   python -m unittest test_app.py
