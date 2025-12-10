#ingestion/expo_backoff.py
import time
import requests

def expo_backoff_request(url, params=None, headers=None, max_retries=5, timeout=15):
    """
    Performs GET request with exponential backoff
    Returns response object if successful, raises last error otherwise.
    """

    delay = 2  #starting delay

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response

        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[BACKOFF] Giving up after {max_retries} attempts")
                raise

            #backoff step
            print(f"[BACKOFF] Attempt {attempt+1} failed: {e}. Retrying in {delay} sec...")
            time.sleep(delay)
            delay *= 2 
