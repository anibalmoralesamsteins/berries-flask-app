from thread_pool import ThreadPoolManager
import logging
from requests import get, exceptions

def fetch_all_berries_concurrently(poke_api_url):
    """Fetch all berries concurrently using the PokeAPI."""
    results = []
    try:
        # Initialize ThreadPoolManager with 10 workers
        # We initialize the ThreadPoolManager here to ensure that it is created only once and on every call to this function.
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
        # This block will always execute, even if an exception is thrown.
        # In this case, it's a good place to clean up the thread pool, but we don't need to do that here
        # as we are managing the shutdown of the thread pool elsewhere.
        logging.info("Completed fetching berry data.")

    return results
