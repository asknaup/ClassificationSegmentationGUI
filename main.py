import base64
from io import BytesIO
import os

from flask import Flask, flash, request, redirect, url_for
from flask import request, escape, render_template, Response
from flask import abort, send_from_directory
from werkzeug.utils import secure_filename
import urllib.request

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

# setting up application figs
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = "secret key"

# Home page
@app.route("/", methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route("/", methods=['GET','POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    # get file name
    file = request.files['file']

    # if file name is empty then upload an image
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
        
    if file and allowed_files(file.filename):
        filename = secure_filename(file.filename)

        file_ext = os.path.split(file.filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Image successfully uploaded and displayed below')

        return render_template('home.html', filename=filename)
    else:
        flash('Allowed image types are: png, jpg, jpeg, gif')
        return redirect(request.url)

# load image and display on home page to preview
@app.route('/display/<filename>')
def display_image(filename):
    # return send_from_directory(app.config['UPLOAD_PATH'], filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)