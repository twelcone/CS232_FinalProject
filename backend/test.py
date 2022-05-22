import requests

resp = requests.post("http://localhost:5000/predict", files={'file': '/home/twel/CS232/backend/test/brain_007.png'})

print(resp.text)