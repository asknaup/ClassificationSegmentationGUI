import imghdr
from io import BytesIO
from PIL import Image
import base64
import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask import send_from_directory, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

app.secret_key = 'This is the secret key'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
@app.route('/home')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    if request.method == 'POST':
        selectedValue = request.form['options']
        return redirect(url_for('click', selectedValue=selectedValue))
    return render_template('home.html', files=files)

@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        # cannot upload .tiff files
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        session['filename'] = filename
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/classification')
def classification():
    filename = session.get('filename', None)
    img_file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    return render_template('classification.html', img_data=img_file_path)

@app.route('/segmentation')
def segmentation():
    filename = session.get('filename', None)
    img_file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    return render_template('segmentation.html', img_data=img_file_path)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)