from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file, flash
import os
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'Das5ahec#23a'

if __name__ == '__main__':
    app.run(debug=True, port=5000)