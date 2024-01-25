import csv
import requests
from bs4 import BeautifulSoup

def scrape_character_info(character):
    url = f"http://www.strokeorder.info/mandarin.php?q={character}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the GIF
        gif_img = soup.find('img', alt=f"stroke order animation of {character}")
        gif_url = gif_img['src'] if gif_img else "GIF not found"
        gif_src = f"<img src='{gif_url}'>" if gif_url != "GIF not found" else "None"

        # Find the table by ID 'pinyin', for the sepcific section of the site
        table = soup.find('td', id='pinyin').find_parent('table')
        if not table:
            return [character, 'Error: Table not found']

        pinyins = []
        definitions = []

        # Iterate over the table rows and collect pinyins and definitions
        for row in table.find_all('tr'):
            pinyin_td = row.find('td', id='pinyin')
            definition_td = row.find('td', id='def')

            if pinyin_td and definition_td:
                pinyins.append(pinyin_td.get_text(strip=True))
                definitions.append(definition_td.get_text(strip=True))
            else:
                break  # If we encounter a row without pinyin/definition, it might be the end of relevant data

        # Combine all pinyins and definitions
        combined_pinyin = "; ".join(pinyins) if pinyins else "Pinyin not found"
        combined_definition = "; ".join(definitions) if definitions else "Definition not found"

        # Radical and Stroke Number
        details = soup.find_all('b')
        radical = details[0].next_sibling.strip() if details else "Radical not found"
        stroke_number = details[1].next_sibling.strip() if details else "Stroke number not found"

        return [character, gif_src, combined_pinyin, radical, stroke_number, combined_definition]
    else:
        return [character, 'Error: Failed to retrieve data']

def format_phrase_data(characters_data, custom_definition=None, example_sentences=None):
    # Formats data for phrases with delimiters
    formatted_data = []
    for i in range(6):  # 6 fields per character
        field_data = [char_data[i] for char_data in characters_data]
        formatted_data.append('|'.join(field_data))

    # Replace definitions with custom definition if provided
    formatted_data[5] = custom_definition if custom_definition else formatted_data[5]

    # Add example sentences at the end
    formatted_data.append(example_sentences if example_sentences else "No example provided")
    return formatted_data

def scrape_word_info(word, custom_definition=None, example_sentences=None):
    characters = list(word)
    characters_data = [scrape_character_info(character) for character in characters]

    if len(characters) > 1:
        return format_phrase_data(characters_data, custom_definition, example_sentences)
    else:
        char_data = characters_data[0]
        char_data[5] = custom_definition if custom_definition else char_data[5]
        char_data.append(example_sentences if example_sentences else "No example provided")
        return char_data

input_file = 'vocab.txt'
output_file = 'anki_import.csv'

with open(input_file, 'r', encoding='utf-8') as file:
    words = [line.strip() for line in file]

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Characters', 'GIF URLs', 'Pinyins', 'Radicals', 'Stroke Numbers', 'Definitions', 'Example Sentences'])

    for line in words:
        line = line.replace("：", ":")  # Standardize format for colon
        if ':' in line:
            parts = line.split('|')
            word_def = parts[0].split(':')
            word = word_def[0].strip()
            custom_definition = word_def[1].strip() if len(word_def) > 1 else None
            example_sentences = '|'.join(parts[1:]).strip() if len(parts) > 1 else None
        else:
            word, custom_definition, example_sentences = line, None, None
        
        row = scrape_word_info(word, custom_definition, example_sentences)
        writer.writerow(row)

print(f"Data sucessfully exported to {output_file}!")
