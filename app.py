import os


from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from ninjadroid import *

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
        path = request.form['path']

        if file.filename == '':
            flash('Не выбран файл для загрузки!1')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            if not os.path.exists(path):
                flash('Не прописан путь для "распаковки" apk или указан несуществующий путь!1')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Файл успешно загружен!0')

            apk = read_target_file(args.target, args.no_string_processing)

            if apk is None:
                sys.exit(1)

            filename = get_apk_filename_without_extension(args.target)
            if args.extract_to_directory is None:
                dumps_apk_info(apk)
            else:
                extract_apk_info_to_directory(apk, args.target, filename, args.extract_to_directory)

            return redirect('/')
        else:
            flash('Принимаются только файлы расширения apk!1')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()
