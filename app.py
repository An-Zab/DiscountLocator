from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('results/contacts.json', 'r', encoding='utf-8') as f:
        contacts = json.load(f)
    return render_template('index.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)