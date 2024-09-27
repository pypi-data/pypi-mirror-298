import requests
import tempfile
import os

def download_pdf_from_url(url):
    """
    Downloads a PDF from the given URL and saves it to a temporary file.
    Returns the path to the temporary file.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    else:
        raise ValueError(f"Failed to download PDF from URL: {url}. Status code: {response.status_code}")

def prompt_func(query, n, role, classes):
    """
    Generates different types of prompts based on the query and role.

    Parameters:
    - query: The user query that needs to be classified or answered.
    - n: Defines which type of prompt is generated (classification, rephrase, etc.).
    - role: The role of the assistant (used in the prompt).
    - classes: Dictionary containing classes/categories for classification.
    
    Returns the generated prompt.
    """
    class_list = ', '.join(f"'{c}'" for c in classes.keys())
    example_list = '. '.join([f"{cls}: {example}" for cls, example in classes.items()])
    
    if n == 1:
        prompt = (
            f"Role: {role}. Please classify the following query into one of the following categories: {class_list}. "
            f"Use the provided examples for accurate classification: {example_list}. "
            "Your response should ONLY be one of the categories provided, with no additional words. "
            f"Query: {query}"
        )
    elif n == 2:
        prompt = "Rephrase the following sentence: I apologize, but I don't have the information you're looking for at the moment."
    elif n == 3:
        prompt = "Rephrase the following sentence: Unfortunately, I am unable to help you with that. Please provide more specific questions related to Voi AI."

    return prompt

def openaiAPI(prompt, temp, openai_key, max_tokens=100):
    """
    Makes a request to the OpenAI API to generate a completion based on the given prompt.

    Parameters:
    - prompt: The prompt to send to OpenAI.
    - temp: Temperature setting for the response generation.
    - openai_key: API key for authentication with OpenAI.
    - max_tokens: Maximum number of tokens to generate in the response.
    
    Returns the category or response from OpenAI.
    """
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_key}',
    }
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI user query classifier that is very experienced. You classify user inputs to one of the provided classes accurately."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temp,
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        category = response.json()['choices'][0]['message']['content'].strip()
        return category
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
