import requests

# The API endpoint
url = "https://xktxdskybynnnzswlkvpgwxiwfb3i89yi.oast.fun"

# A GET request to the API
response = requests.get(url)

# Print the response
print(response.json())