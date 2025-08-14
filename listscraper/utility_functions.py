# Some utility functions are stored here
import requests
import time

def stars2val(stars, not_found):
    """
    Transforms star rating into float value.
    """
    
    conv_dict = {
        "★": 1.0,
        "★★": 2.0,
        "★★★": 3.0,
        "★★★★": 4.0,
        "★★★★★": 5.0,
        "½": 0.5,
        "★½": 1.5,
        "★★½": 2.5,
        "★★★½": 3.5,
        "★★★★½": 4.5 }

    try:
        val = conv_dict[stars]
        return val
    except:
        return not_found
    
def val2stars(val, not_found):
    """
    Transforms float value into star string.
    """
    conv_dict = {
        1.0 : "★",
        2.0 : "★★",
        3.0 : "★★★",
        4.0 : "★★★★",
        5.0 : "★★★★★",
        0.5 : "½",
        1.5 : "★½",
        2.5 : "★★½",
        3.5 : "★★★½",
        4.5 : "★★★★½" }
    try:
        stars = conv_dict[val]
        return stars
    except:
        return not_found

def repeated_request(url):
    """
    Makes a request to a URL with exponential backoff for 429 errors.

    Args:
        url (str): The URL to make a request to.

    Returns:
        requests.Response: The successful response object.

    Raises:
        requests.exceptions.RequestException: If the request fails after all retries.
    """
    retries = 0
    max_retries = 5
    current_delay = 8
    max_delay = 120  # 2 minutes in seconds

    while retries < max_retries:
        try:
            response = requests.get(url)
            
            # Check for a 429 "Too Many Requests" error
            if response.status_code == 429:
                print(f"Received 429 response. Retrying in {current_delay} seconds...")
                time.sleep(current_delay)
                
                # Double the delay for the next attempt, capped at max_delay
                current_delay = min(current_delay * 2, max_delay)
                retries += 1
                continue  # Skip to the next iteration of the while loop
            
            # If the request is successful, or another error occurs, break the loop
            response.raise_for_status()
            #print("Request successful!")
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during request: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {current_delay} seconds...")
                time.sleep(current_delay)
                current_delay = min(current_delay * 2, max_delay)
            else:
                print("Max retries exceeded. Giving up.")
                raise # Re-raise the last exception

    print(f"Request failed after all retries. Server status code: {response.status_code}")
    raise requests.exceptions.RequestException(f"Request failed after all retries. Server status code: {response.status_code}")
