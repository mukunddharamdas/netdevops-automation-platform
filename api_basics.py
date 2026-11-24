import requests

url = "https://httpbin.org/json"

try:
    response = requests.get(url, timeout=10)
    print(f"Status code received: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    print("API response retrieved and parsed successfully")
    print(f"Response size: {len(response.content)} bytes")

except requests.exceptions.Timeout:
    print("ERROR - API request timed out")

except requests.exceptions.HTTPError as error:
    print(f"ERROR - HTTP error: {type(error).__name__}")

except requests.exceptions.JSONDecodeError:
    print("ERROR - API returned invalid JSON")

except requests.exceptions.RequestException as error:
    print(f"ERROR - API request failed: {type(error).__name__}")