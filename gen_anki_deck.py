import genanki
import csv

# Ask the user for the deck name
deck_name = input("Enter the name for the Anki deck: ")

my_model = genanki.Model(
    1607392319,
    'Chinese Characters Model',
    fields=[
        {'name': 'Characters'},
        {'name': 'GIF URLs'},
        {'name': 'Pinyins'},
        {'name': 'Radicals'},
        {'name': 'Stroke Numbers'},
        {'name': 'Definitions'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Definitions}}',  # Front of card shows the definitions
            'afmt': '''
                <div><strong>Character(s):</strong> {{Characters}}</div>
                <div>{{GIF URLs}}</div>
                <hr id="answer">
                <div><strong>Pinyin:</strong> {{Pinyins}}</div>
                <div><strong>Radical:</strong> {{Radicals}}</div>
                <div><strong>Stroke Number:</strong> {{Stroke Numbers}}</div>
            ''',  # Back of card shows the characters and other details
        },
    ],
    css='''
        .card {
            font-family: arial;
            font-size: 20px;
            text-align: center;
            color: black;
            background-color: white;
        }
        img {
            max-height: 100px;
        }
    '''
)


# Create a new deck
my_deck = genanki.Deck(
    2059400110,
    deck_name
)

# Path to your CSV file
csv_file_path = 'anki_import.csv'

# Function to process phrase data
def process_phrase_data(row):
    if '|' in row[0]:  # If it's a phrase
        row[0] = ''.join(row[0].split('|'))  # Remove delimiter in Characters field
    return row

# Read the CSV file and add notes to the deck
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip the header row

    for row in reader:
        processed_row = process_phrase_data(row)
        my_note = genanki.Note(
            model=my_model,
            fields=processed_row
        )
        my_deck.add_note(my_note)

# Save the deck to an .apkg file
output_file = f'{deck_name.replace(" ", "_")}.apkg'
genanki.Package(my_deck).write_to_file(output_file)

print(f"Deck '{deck_name}' has been created as {output_file}")
