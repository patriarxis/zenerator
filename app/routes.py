from flask import render_template, request
from haiku.generator import generate_haiku
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        github_repo_url = request.form.get('github_repo_url')

        haiku = generate_haiku(text_input, github_repo_url)

        return render_template('haiku.html', haiku=haiku)

    return render_template('index.html')
