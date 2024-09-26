import json
import os
import base64
import requests



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

def answer_formatting(text):
    # Find the indices of the triple single quotes
    start_index = text.find("```json") + len("```json")
    end_index = text.rfind("```")

    # Slice the string to get the content between the quotes
    content_between = text[start_index:end_index]

    # Remove newline characters
    text_formatted = content_between.replace('\n', '')

    return text_formatted

def save_to_json(text, file_name):
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


def text_extraction_OpenAI(image_path, message, key):
    # assigning API KEY to initialize openai environment
    api_key = key
    # Getting the base64 string
    base64_image = encode_image(image_path)
    file_name_without_extension = os.path.splitext(os.path.basename(image_path))[0]

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4o-mini",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": message
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    formatted_text = answer_formatting(response.json()["choices"][0]["message"]['content'])
    save_to_json(formatted_text, file_name_without_extension)


    return response.json()["choices"][0]["message"]['content']

