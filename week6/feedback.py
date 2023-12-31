import requests
import json
from train import X_test, y_test

URL = "http://localhost:9000/api/v1.0/feedback"


def send_prediction_feedback(data):
    # Create the headers for the request
    headers = {'Content-Type': 'application/json'}

    try:
        # Send the POST request
        response = requests.post(URL, headers=headers, json=data)

        # Check if the request was successful
        response.raise_for_status()  # Will raise HTTPError if the HTTP request returned an unsuccessful status code

        # If successful, return the JSON data
        return response.json()
    except requests.ConnectionError:
        raise Exception("Failed to connect to the server. Is it running?")
    except requests.Timeout:
        raise Exception("Request timed out. Please try again later.")
    except requests.RequestException as err:
        # For any other requests exceptions, re-raise it
        raise Exception(f"An error occurred with your request: {err}")


for i in range(len(X_test)):
    payload = {'request': {'data': {'ndarray': [X_test[i].tolist()]}}, 'truth': {'data': {'ndarray': [int(y_test[i])]}}}

    try:
        response = send_prediction_feedback(payload)
        pretty_json_response = json.dumps(response, indent=4)  # Pretty-print JSON
        print(pretty_json_response)
    except Exception as err:
        print(err)