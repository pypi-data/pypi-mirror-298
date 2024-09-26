import os
from mistralai import Mistral
import base64
import json


def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def text_formatting(text):
    # Remove newline characters
    content_to_save_no_newlines = text.replace('\n', '')

    return content_to_save_no_newlines


def save_to_json(text, image_path):
    structured_data = {}

    # Attempt to load the modified string as JSON
    try:
        structured_data = json.loads(text)  # Convert string to Python dict/list
        print("Successfully parsed JSON.")
    except json.JSONDecodeError as e:
        print("Error: The response content is still not valid JSON after removing newlines.")
        print(f"JSONDecodeError: {e}")

    # Save the structured data to a JSON file
    try:
        with open(f'./data/json_openAI/{file_name}.json', 'w', encoding='utf-8') as json_file:
            if structured_data != {}:
                json.dump(structured_data, json_file, indent=4,
                          ensure_ascii=False)  # `indent=4` for pretty printing
    except FileNotFoundError:
        print(f"Error: The file ./data/json_openAI/{file_name} was not found.")


def text_extraction_Pixtral(image_path, message, key):
    api_key = key
    model = "pixtral-12b-2409"
    client = Mistral(api_key=api_key)
    base64_image = encode_image(image_path)
    file_name = os.path.splitext(os.path.basename(image_path))[0]


    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ],
            "response_format":
                {
                    "type": "json_object"
                }
        }
    ]

    chat_response = client.chat.complete(
        model=model,
        messages=messages,
        response_format = {
            "type": "json_object",
        }
    )

    # Get the content
    content_to_save = chat_response.choices[0].message.content

    formatted_text = text_formatting(content_to_save)

    save_to_json(formatted_text, file_name)



    return content_to_save
