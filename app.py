import os
import sys
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from helper.blob_directory_interface import DirectoryClient

try:
    CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
except KeyError:
    print('AZURE_STORAGE_CONNECTION_STRING must be set')
    sys.exit(1)

try:
    CONTAINER_NAME = sys.argv[1]
except IndexError:
    print('usage: directory_interface.py CONTAINER_NAME')
    print('error: the following arguments are required: CONTAINER_NAME')
    sys.exit(1)

client = DirectoryClient(CONNECTION_STRING, CONTAINER_NAME)
dirs = client.ls_dirs('')
print(dirs)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            client.upload(filename, filename)
            msg = 'Uploading file: ' + filename

    return render_template('index.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
