import os, io
from google.cloud import vision, texttospeech
from google.cloud.vision_v1 import types
from spellchecker import SpellChecker
from textblob import Word

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'pleasedontmine.json'

def get_handwritten(filename):
    client = vision.ImageAnnotatorClient()  

    FOLDER_PATH = os.getcwd()+ '/templates/Images'
    IMAGE_FILE = filename
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text

    text = docText.lower().replace('.', '').replace('(', '').replace(')', '').replace(',', '').replace('--', ' ').replace('-', ' ').replace(':', '').replace(';', '').replace('? ', '.').replace('!', '.').replace('\n', ' ').split()

    return(text)

def get_corrections(text):
    spell = SpellChecker()
    corrections = {}

    for flagged_word in spell.unknown(text):
        word = Word(flagged_word)
        choices = []
        
        for choice in word.spellcheck():
            if choice[1] > 0.05 and len(choices) <= 4 and flagged_word != choice[0]:
                choices.append(choice[0])

        if len(choices) > 0:
            corrections[flagged_word] = choices
    return corrections

def get_speech(output_name, options):
    phrase = "........ , ........ , ........ , ........ , ........ ".join(options)

    client = texttospeech.TextToSpeechClient()

    FOLDER_PATH = os.getcwd() + '/Audio'
    AUDIO_FILE = output_name + '.mp3'
    FILE_PATH = os.path.join(FOLDER_PATH, AUDIO_FILE)

    synthesis_input = texttospeech.SynthesisInput(text=phrase)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(FILE_PATH, "wb") as out:
        out.write(response.audio_content)


    
