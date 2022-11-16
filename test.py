import requests

response = requests.get("http://localhost:8000/user/1")
print(response)