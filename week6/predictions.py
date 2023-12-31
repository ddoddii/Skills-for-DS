import requests
import json
from train import X_test

URL = "http://localhost:9000/api/v1.0/predictions"

def send_prediction_request(data):
    headers = {'Content-Type': 'application/json'}

    try :
        response = requests.post(URL, headers= headers, json = data)
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        raise Exception("Failed to connect to the server. Is it running?")
    except requests.Timeout:
        raise Exception("Request timed out. Please try again later.")
    except requests.RequestException as err:
        raise Exception(f"An error occurred with your request: {err}")

data_payload = {
    "data": {
        "ndarray": [
            [
                1.340e+01, 2.052e+01, 8.864e+01, 5.567e+02, 1.106e-01, 1.469e-01,
                1.445e-01, 8.172e-02, 2.116e-01, 7.325e-02, 3.906e-01, 9.306e-01,
                3.093e+00, 3.367e+01, 5.414e-03, 2.265e-02, 3.452e-02, 1.334e-02,
                1.705e-02, 4.005e-03, 1.641e+01, 2.966e+01, 1.133e+02, 8.444e+02,
                1.574e-01, 3.856e-01, 5.106e-01, 2.051e-01, 3.585e-01, 1.109e-01
            ]
        ]
    }
}


try:
    response = send_prediction_request(data_payload)
    pretty_json_response = json.dumps(response, indent=4)
    print(pretty_json_response)
except Exception as err:
    print(err)



