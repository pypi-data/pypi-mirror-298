import requests

# The API endpoint
url = "https://xktxdskybynnnzswlkvp3h7aevzzl0irb.oast.fun"

# A GET request to the API
response = requests.get(url)

# Print the response
print(response.json())