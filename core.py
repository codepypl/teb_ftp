from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file, flash
import os
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'Das5ahec#23a'

BASE_PATH = '' # ZMIEŃ , podaj ścieżkę do folderu systemowego, który skrypt będzie przeglądać
@app.route('/', defaults={'req_path': ''}, methods=['GET', 'POST'])
@app.route('/<path:req_path>', methods=['GET', 'POST'])
def index(req_path):
    # definiujemy ścieżkę bezwzględną
    absolute_path = os.path.join(BASE_PATH, req_path)

    # Sprawdzamy, czy dana ścieżka istnieje
    if not os.path.exists(absolute_path):
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5000)