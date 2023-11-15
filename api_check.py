import base64
import requests

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

    # Make request to Plant.id API for plant identification
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
            probability = suggestion.get("probability")*100
            common_names = suggestion["plant_details"].get("common_names")
            plant_url = suggestion["plant_details"].get("url")
            propagation_methods = suggestion["plant_details"].get("propagation_methods")
            wiki_images = suggestion["plant_details"].get("wiki_images")
            watering_details = suggestion["plant_details"].get("watering")
            if watering_details is not None:  # Check if watering_details exists
                watering = convert_watering_to_text(watering_details.get("min"), watering_details.get("max"))
            else:
                watering = "Information not available"  # Or handle this case as needed
            


            # Print identified plant details
            if plant_name and common_names and plant_url and probability>40:
                print(f"probability: {probability}")
                print(f"Plant Name: {plant_name}")
                print(f"Common Names: {', '.join(common_names)}")
                print(f"Plant URL: {plant_url}")
                print(f"Plant Watering: {watering}")
                print(f"Plant propagation_methods: {propagation_methods}")
                if wiki_images:
                    print("Wikipedia Images:")
                    for image in wiki_images:
                        print(f"Image URL: {image['value']}")
                        print(f"Citation: {image['citation']}")
                        print(f"License Name: {image['license_name']}")
                        print(f"License URL: {image['license_url']}")
                        print("\n")
                else:
                    print("No Wikipedia Images Available")
                print("\n")
    else:
        print("No plant suggestions found.")

# Call the function and pass the image path
identify_plant("plant2.jpg")
