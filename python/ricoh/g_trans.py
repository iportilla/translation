# Import necessary libraries
from googletrans import Translator
from bs4 import BeautifulSoup

import os
import time
import argparse

# Initialize parser
parser = argparse.ArgumentParser(description="Translate HTML files to a specified language.")

# Adding required arguments
parser.add_argument("input_file", help="Path to the input HTML file.")
parser.add_argument("output_file", help="Path to the output (translated) HTML file.")
parser.add_argument("language", help="Target language code (e.g., 'en' for English, 'de' for German).")

# Parse arguments
args = parser.parse_args()

# Update the variables to use the parsed arguments
html_file_path = args.input_file
translated_html_file = args.output_file
destination_language = args.language

# Rest of the script remains the same


# Initialize the Translator
translator = Translator()

def translate_text(text, dest_language='en'):
    """
    Translate a given text to the specified language.
    
    Parameters:
    - text (str): Text to translate.
    - dest_language (str): Target language code (default is English 'en').
    
    Returns:
    - str: Translated text.
    """
    try:
        # Translate the text
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        # Print error and return original text if translation fails
        print(f"Error translating text: {e}")
        return text

def translate_html_file(file_path, dest_language='en'):
    """
    Translate the content of an HTML file to the specified language.
    
    Parameters:
    - file_path (str): Path to the HTML file.
    - dest_language (str): Target language code.
    
    Returns:
    - str: Path to the translated HTML file.
    """
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Translate each text element in the HTML
        for element in soup.find_all(text=True):
            if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                original_text = element.string
                translated_text = translate_text(original_text, dest_language)
                element.string.replace_with(translated_text)
    
    # Create a path for the translated HTML file
    translated_file_path = os.path.splitext(file_path)[0] + f'_translated_{dest_language}.html'
    
    # Write the translated content to a new file
    with open(translated_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    return translated_file_path

# Define source and target HTML file paths and the destination language
# html_file_path = './bemo-index.html'
# destination_language = 'de'

# Measure the time taken to translate the file
start_time = time.time()

print(f"Translating HTML file to {destination_language}...")
translated_html_path = translate_html_file(html_file_path, destination_language)
print(f"Translated HTML file saved at: {translated_html_path}")

end_time = time.time()
print(f"Translation completed in {end_time - start_time} seconds.")