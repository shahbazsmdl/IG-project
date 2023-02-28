import requests
import openai
import facebook
import random
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
facebook_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

instagram_access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")

# Connect to Facebook API
graph = facebook.GraphAPI(access_token=facebook_access_token, version="3.0")

# Define the API endpoint for image generation
image_endpoint = "https://api.openai.com/v1/images/generations"

# Define the API headers for image generation
image_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}

def generate_prompt():
    topics = ["beaches", "town", "beautiful agriculture area", "beautiful places"]
    selected_topic = random.choice(topics)

    # Generate the text prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"topic: {selected_topic} select any {selected_topic} and tell me about the {selected_topic} where it is and why? [Instragram discription][15 hash tage][emoji]",
        max_tokens=220,
        temperature=0.5
    )
    prompt_text = response["choices"][0]["text"].strip()
    return prompt_text

def generate_image(prompt):
    # Define the API request data for image generation
    image_data = {
        "model": "image-alpha-001",
        "prompt": f"Generate a high-resolution, visually stunning ,relistic,No human,No text. Description: {prompt}. Your goal is to create an image that is visually striking and eye-catching, ultra-detailed, ultrarealistic, photorealism, 8k, octane render",
        "size": "1024x1024"
    }

    # Send the API request for image generation
    image_response = requests.post(image_endpoint, headers=image_headers, json=image_data)

    # Check the API response status for image generation
    if image_response.status_code == 200:
        # Extract the URL of the generated image
        image_url = image_response.json()["data"][0]["url"]
        return image_url
    else:
        # Print the API error message
        print(f"Error: {image_response.json()['message']}")
        return None
def upload_to_facebook(prompt, image_url):
# Upload the generated image to Facebook
     message =f"{prompt}"
     print(image_url)
     graph.put_object(parent_object='me', connection_name='feed',message=message,link=image_url)
def upload_to_instagram(prompt, image_url):
# Upload the generated image to Instagram
    ig_user_id=17841458248364449
    access_token=instagram_access_token
    # Step 1 of 2: Create Container
    media_url = f"https://graph.facebook.com/v16.0/{ig_user_id}/media"
    params = {
        "image_url": image_url,
        "caption": prompt,
        "access_token": access_token
    }
    response = requests.post(media_url, params=params)
    media_id = response.json().get("id")
    
    # Step 2 of 2: Publish Container
    publish_url = f"https://graph.facebook.com/v16.0/{ig_user_id}/media_publish"
    params = {
        "creation_id": media_id,
        "access_token": access_token
    }
    response = requests.post(publish_url, params=params)
    print(response.json())

def generate_and_upload_image():

    
    # Define possible prompts for the image generation
    prompt = generate_prompt()
    print(prompt)
    image_url = generate_image(prompt)
    if image_url:
    #   upload_to_facebook(prompt, image_url)
      print(image_url)
      upload_to_instagram(prompt, image_url)
generate_and_upload_image()
