import requests as r

url = "http://0.0.0.0:8000/predict"

data = {
    "input": "https://www.lizsteel.com/wp-content/uploads/2016/02/LizSteel-160223-Handwriting.jpg"
}

response = r.post(url, json=data)
print(response.json())
