import requests

url = "https://httpbin.org/html"

try:
    response = requests.get(url, timeout=10)
    print(f"Status code received: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(data)

except requests.exceptions.Timeout:
    print("ERROR - API request timed out")

except requests.exceptions.HTTPError as error:
    print(f"ERROR - HTTP error: {error}")

except requests.exceptions.JSONDecodeError:
    print("ERROR - API returned invalid JSON")

except requests.exceptions.RequestException as error:
    print(f"ERROR - API request failed: {error}")