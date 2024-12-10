from thread_pool import ThreadPoolManager
import logging
from requests import get, exceptions
import os

def fetch_all_berries_sequentially(poke_api_url):
    """Fetch all berries sequentially using the PokeAPI."""
    results = []
    try:
        # Fetch the initial berry data
        response = get(f"{poke_api_url}/berry")
        response.raise_for_status()  # Will raise an HTTPError if the response is 4xx/5xx
        data = response.json()
        url_results = data["results"]

        # Handle pagination if more results are available
        while data["next"]:
            response = get(data["next"])
            response.raise_for_status()
            data = response.json()
            url_results.extend(data["results"])

        # Fetch berry details sequentially
        for url_result in url_results:
            response = get(url_result["url"])
            response.raise_for_status()
            results.append(response.json())

    except exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching data from PokeAPI: {e}")
        raise  # Re-raise the exception to propagate it up

    finally:
        logging.info("Completed fetching berry data sequentially.")

    return results

def fetch_all_berries_concurrently(poke_api_url):
    """Fetch all berries concurrently using the PokeAPI."""
    results = []
    try:
        # Initialize ThreadPoolManager with 10 workers
        thread_pool_manager = ThreadPoolManager(max_workers=10)

        # Fetch the initial berry data
        response = get(f"{poke_api_url}/berry")
        response.raise_for_status()  # Will raise an HTTPError if the response is 4xx/5xx
        data = response.json()
        url_results = data["results"]

        # Handle pagination if more results are available
        while data["next"]:
            response = get(data["next"])
            response.raise_for_status()
            data = response.json()
            url_results.extend(data["results"])

        # Fetch berry details concurrently using thread pool
        results = thread_pool_manager.fetch_all_concurrently([url_result["url"] for url_result in url_results])

    except exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching data from PokeAPI: {e}")
        raise  # Re-raise the exception to propagate it up

    finally:
        logging.info("Completed fetching berry data concurrently.")

    return results

def fetch_all_berries(poke_api_url):
    """Fetch all berries based on the FETCH_MODE environment variable."""
    fetch_mode = os.getenv('FETCH_MODE', 'concurrent').lower()
    if fetch_mode == 'sequential':
        return fetch_all_berries_sequentially(poke_api_url)
    else:
        return fetch_all_berries_concurrently(poke_api_url)
