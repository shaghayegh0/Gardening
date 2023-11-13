import base64
import requests

# encode images to base64
with open("ill_plant.jpg", "rb") as file:
    images = [base64.b64encode(file.read()).decode("ascii")]

response = requests.post(
    "https://api.plant.id/v2/health_assessment",
    json={
        "images": images,
        "modifiers": ["similar_images"],
        "disease_details": ["description", "treatment"],
    },
    headers={
        "Content-Type": "application/json",
        "Api-Key": "ljctzrgXKznCd9RsRxCD4Mu0HOfulDay9UkjlrNnwUKnNi5ruw",
    }).json()

if not response["health_assessment"]["is_healthy"]:
    for suggestion in response["health_assessment"]["diseases"]:
        print(suggestion["name"])   # water deficiency
        print(suggestion["disease_details"]["description"])    # Water deficiency is...