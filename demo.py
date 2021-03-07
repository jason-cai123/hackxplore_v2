import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types
from spellchecker import SpellChecker
from textblob import Word

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'pleasedontmine.json'

def get_handwritten(filename):
    client = vision.ImageAnnotatorClient()  

    FOLDER_PATH = os.getcwd()+ '/Images'
    IMAGE_FILE = filename
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text
    
    print(docText)

    return docText

def get_corrections(docText):
    text = docText.lower().replace('.', '').replace('(', '').replace(')', '').replace(',', '').replace('--', ' ').replace('-', ' ').replace(':', '').replace(';', '').replace('? ', '.').replace('!', '.').replace('\n', ' ').split()
    print(text)

    spell = SpellChecker()
    corrections = {}

    print(spell.unknown(text))
    for flagged_word in spell.unknown(text):
        word = Word(flagged_word)
        choices = []
        for choice in word.spellcheck():
            if choice[1] > 0.05 and len(choices) <= 4:
                choices.append(choice[0])

        if len(choices) > 0:
            corrections[flagged_word] = choices
            
    print(corrections)
        
    return corrections
    
if __name__ == "__main__":
    get_handwritten()
