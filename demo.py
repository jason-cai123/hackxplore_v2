import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types

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
    #print(docText)
    return docText

if __name__ == "__main__":
    get_handwritten()
