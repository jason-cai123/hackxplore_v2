import os, io
from flask import Flask, jsonify, flash, request, redirect, url_for, render_template, send_from_directory
from demo import get_handwritten, get_corrections, get_speech
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

UPLOAD_FOLDER = os.getcwd()+'/templates/Images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = ['jpg','jpeg']

def allowed_file(filename):
    return'.' in filename and filename.rsplit('.',1) [1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_sentence(filename):
    handwritten = get_handwritten(filename)
    corrections = get_corrections(handwritten)
    #print(corrections, file=sys.stderr)

    sentence = []
    for word in handwritten:
        if corrections.get(word, 0) != 0:
            sentence.append([word, corrections[word]])
        else:
            sentence.append([word, None])
    '''
    for word in handwritten:
        if corrections.get(word, 0) != 0:
            sentence.append({word : corrections[word]})
        else:
            sentence.append({word : None})
    '''
    return sentence
    

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None:
            print('no file part', file=sys.stderr)
            flash('No file part')
            return redirect(request.url)
        
        elif file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            PATH = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(PATH)
            print(filename, file=sys.stderr)

            #sentence = get_sentence(filename)
            #print(sentence, file=sys.stderr)

            '''
            for word,options in corrections.items():
                get_speech(word, options)
            '''

            photo = filename
            #print(photo)
            #photo = redirect(url_for('uploaded_file', filename=filename))

            #return handwritten

        #return redirect(url_for('text', writing=sentence, photo=photo))
        return redirect(url_for('text', photo=photo))

        #return redirect(url_for('uploaded_file',
                               # filename=filename))
    return render_template("upload.html")

#@app.route('/text/<list:writing>/<string:photo>', methods=['POST', 'GET'])
#def text(writing, photo):#
@app.route('/text/<string:photo>', methods=['POST', 'GET'])
def text(photo):
    #filename = "templates/Images/" + photo
    writing = get_sentence(photo)
    filename = 'http://127.0.0.1:5000/uploads/' + photo
    return render_template("text.html", writing=writing, photo=filename)

'''
@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('template.html', filename=filename)
'''

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run()