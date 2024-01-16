# Chinese Character Anki Deck Generator

This Python project automates the creation of Anki flashcards for studying Chinese characters. It scrapes character data from a specified website, generates a CSV file with the gathered information, and then uses this data to create a custom Anki deck.

## Features

- **Data Scraping**: Automatically scrapes Chinese character information, including GIFs of stroke order, pinyin, definitions, radicals, and stroke numbers.
- **CSV Generation**: Organizes scraped data into a CSV file, with support for both single characters and phrases.
- **Anki Deck Creation**: Generates an Anki deck from the CSV data, with cards formatted to show the definition on the front and additional details on the back.

## How to Use

1. **Prepare the Vocabulary List**: Create a text file named `vocab.txt` with the list of Chinese characters or phrases you wish to study, with each entry on a new line.

2. **Run the Script**: Execute the script using a Python interpreter. The script will prompt you for the name of the Anki deck.

    ```bash
    python chinese_anki_generator.py
    ```

3. **Import Anki Deck**: After the script finishes, import the generated `.apkg` file into Anki.
