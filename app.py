from flask import Flask, render_template, request
import base64
import requests

app = Flask(__name__)

def convert_watering_to_text(min_val, max_val):
    watering_descriptions = {
        1: "dry",
        2: "medium",
        3: "wet"
    }

    min_desc = watering_descriptions.get(min_val)
    max_desc = watering_descriptions.get(max_val)

    if min_desc and max_desc:
        return f"{min_desc} to {max_desc}"
    else:
        return "Information not available"

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
            # print(plant_name)

            # convert probability to percentage
            probability = suggestion.get("probability")*100

            # a list "common_names": ["Common dandelion", "Dandelion"]
            common_names = suggestion["plant_details"].get("common_names")

            plant_url = suggestion["plant_details"].get("url")

            # {min:1, max:2}
            watering_details = suggestion["plant_details"].get("watering")
            if watering_details is not None:  # Check if watering_details exists
                watering = convert_watering_to_text(watering_details.get("min"), watering_details.get("max"))
            else:
                watering = "Information not available"  # Or handle this case as needed

            
            # contains a list of propagation methods.
            propagation_methods = suggestion["plant_details"].get("propagation_methods")
            
            wiki_images = suggestion["plant_details"].get("wiki_images")
            if wiki_images:
                    for image in wiki_images:
                        image_value =  {image['value']}
                        image_citation = {image['citation']}
                        image_license_name = {image['license_name']}
                        image_license_url = {image['license_url']}


    else:
        
        return ("No plant suggestions found.")

@app.route('/')
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
            details = identify_plant(file_path)

            # Pass the identified details to the HTML template
            return render_template('result.html', details = details)

if __name__ == '__main__':
    app.run(debug=True)