import os, io
from flask import Flask, jsonify, flash, request, redirect, url_for, render_template, send_from_directory
from demo import get_handwritten
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

UPLOAD_FOLDER = os.getcwd()+'/Images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = ['jpg','jpeg']

def allowed_file(filename):
    return'.' in filename and filename.rsplit('.',1) [1].lower() in app.config['ALLOWED_EXTENSIONS']

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

            handwritten = get_handwritten(filename)
            print(handwritten, file=sys.stderr)

            return handwritten
        
        #return redirect(url_for('uploaded_file',
                               # filename=filename))
    return render_template("upload.html")

if __name__ == '__main__':
    app.run()