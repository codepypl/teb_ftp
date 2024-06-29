from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file, flash
import os
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'Das5ahec#23a'


BASE_PATH = '/Users/shadi/Desktop/ftp'  # ZMIEŃ, podaj ścieżkę do folderu systemowego, który skrypt będzie przeglądać


@app.route('/', defaults={'req_path': ''}, methods=['GET', 'POST'])
@app.route('/<path:req_path>', methods=['GET', 'POST'])
def index(req_path):
    # definiujemy ścieżkę bezwzględną
    absolute_path = os.path.join(BASE_PATH, req_path)

    # Sprawdzamy, czy dana ścieżka istnieje
    if not os.path.exists(absolute_path):
        return abort(404)

    # Listowanie katalogu
    files = os.listdir(absolute_path)

    # Tworzenie nowego katalogu
    if request.method == 'POST' and 'new_dir_name' in request.form:
        new_dir_name = request.form['new_dir_name']
        if new_dir_name:
            new_dir_path = os.path.join(absolute_path, new_dir_name)
            try:
                os.mkdir(new_dir_path)
            except Exception as e:
                print(e)
        return redirect(url_for('index', req_path=req_path))

    # Przesyłanie plików
    if request.method == 'POST' and 'file' in request.form:
        files = request.files.getlist('file')
        for file in files:
            if file:
                file_path = os.path.join(absolute_path, file.filename)
                try:
                    file.save(file_path)
                except Exception as e:
                    flash(f"Nie udało się przesłać pliku: {str(e)}", 'error')
        return redirect(url_for('index', req_path=req_path))

    # Pobieranie plików
    if request.method == 'POST' and 'download_files' in request.form:
        selected_files = request.form.getlist('selected_files')
        if selected_files:
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for file_name in selected_files:
                    file_path = os.path.join(absolute_path, file_name)
                    zf.write(file_path, os.path.basename(file_path))
            memory_file.seek(0)
            return send_file(memory_file, download_name='files.zip', as_attachment=True)


    # renderowanie widoku
    return render_template('index.html', files=files, current_path=req_path)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
