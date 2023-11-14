from flask import Flask, render_template
import base64
import requests

app = Flask(__name__)

def identify_plant(image_path):
    # Encode image to base64
    with open(image_path, "rb") as file:
        images = [base64.b64encode(file.read()).decode("ascii")]

    response = requests.post(
        "https://api.plant.id/v2/identify",
        json={
            "images": images,
            "modifiers": ["similar_images"],
            "plant_details": ["common_names", "watering", "propagation_methods ", "url" , "wiki_images"],
        },
        headers={
            "Content-Type": "application/json",
            "Api-Key": "ljctzrgXKznCd9RsRxCD4Mu0HOfulDay9UkjlrNnwUKnNi5ruw",  
        }).json()

    # Process the API response
    if "suggestions" in response:
        for suggestion in response["suggestions"]:
            plant_name = suggestion.get("plant_name")
            probability = suggestion.get("probability")
            common_names = suggestion["plant_details"].get("common_names")
            plant_url = suggestion["plant_details"].get("url")
            watering = suggestion["plant_details"].get("watering")
            propagation_methods = suggestion["plant_details"].get("propagation_methods")
            wiki_images = suggestion["plant_details"].get("wiki_images")
            if wiki_images:
                    for image in wiki_images:
                        image_value =  {image['value']}
                        image_citation = {image['citation']}
                        image_license_name = {image['license_name']}
                        image_license_url = {image['license_url']}


    else:
        print("No plant suggestions found.")


def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file temporarily
            file_path = "temp.jpg"
            file.save(file_path)

            # Identify the plant
            identified_plant_details = identify_plant(file_path)

            # Pass the identified details to the HTML template
            return render_template('result.html', details=identified_plant_details)

if __name__ == '__main__':
    app.run(debug=True)