from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import get
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ThreadPoolManager:
    def __init__(self, max_workers=10):
        """Initialize the ThreadPoolExecutor with the given number of workers."""
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def fetch_data(self, url):
        """Fetch data from a URL."""
        try:
            response = get(url)
            response.raise_for_status()  # Raise an error for bad HTTP status
            return response.json() if response.ok else None
        except Exception as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return None

    def fetch_all_concurrently(self, urls):
        """
        Fetch data concurrently for a list of URLs.
        Each URL will be processed in parallel using the thread pool.
        """
        futures = []
        try:
            # Submit all the tasks to the thread pool
            for url in urls:
                futures.append(self.executor.submit(self.fetch_data, url))
            
            results = []
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                else:
                    logger.warning("Failed to fetch data for some URLs.")
            
            return results
        
        except Exception as e:
            logger.error(f"Error during concurrent fetching: {e}")
            raise

        finally:
            # Ensure the thread pool is shut down, regardless of exceptions
            self.shutdown()

    def shutdown(self):
        """Shutdown the executor when done."""
        try:
            self.executor.shutdown(wait=True)  # Wait for all threads to finish
            logger.info("ThreadPoolExecutor has been shut down.")
        except Exception as e:
            logger.error(f"Error shutting down the ThreadPoolExecutor: {e}")
