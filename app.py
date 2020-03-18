import os


from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from logic import *

ALLOWED_EXTENSIONS = {'apk'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # проверка на файл пост запросом
        if 'file' not in request.files:
            flash('Нет файловой части!1')
            return redirect(request.url)

        if 'path' not in request.form:
            flash('Нет указанного пути!1')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Не выбран файл для загрузки!1')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Файл успешно загружен!0')

            complete_apk_analyze(os.path.join(app.config['UPLOAD_FOLDER'], filename), "./uploads/")

            return redirect('/')
        else:
            flash('Принимаются только файлы расширения apk!1')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()
