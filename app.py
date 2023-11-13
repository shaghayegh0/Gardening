from flask import Flask, render_template
import base64
import requests

app = Flask(__name__)

@app.route('/')
def index():
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

    diseases = []
    if not response["health_assessment"]["is_healthy"]:
        diseases = response["health_assessment"]["diseases"]

    return render_template('index.html', diseases=diseases)

if __name__ == '__main__':
    app.run(debug=True)
