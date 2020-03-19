import os
import sys
import shutil


from flaskwebgui import FlaskUI
from flask import Flask, send_file, request, redirect, render_template
from werkzeug.utils import secure_filename
from logic import *
from zipfile import ZipFile

ALLOWED_EXTENSIONS = {'apk'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

ui = FlaskUI(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Zip the files from given directory that matches the filter
def zipFilesInDir(dirName, zipFileName):
    # create a ZipFile object
    with ZipFile(zipFileName, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)


@app.route('/')
def upload_form():
    shutil.rmtree('./uploads/')
    os.mkdir('uploads')
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # проверка на файл пост запросом
        if 'file' not in request.files:
            flash('Нет файловой части!1')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Не выбран файл для загрузки!1')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            f = complete_apk_analyze(os.path.join(app.config['UPLOAD_FOLDER'], filename), "./uploads/")
            print(f"{f} - foldename")

            zipFilesInDir(f"./uploads/{f}", f"./uploads/{f}.zip")

            return send_file(f'./uploads/{f}.zip', attachment_filename=f'{f}.zip')

        else:
            flash('Принимаются только файлы расширения apk!1')
            return redirect(request.url)


if __name__ == "__main__":
    ui.run()
