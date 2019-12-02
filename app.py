from flask import Flask,send_file
from jinja2 import Environment, FileSystemLoader, select_autoescape
from event import Event
import requests, json

app = Flask('posters')
env = Environment(
    loader= FileSystemLoader('./templates'),
    autoescape=select_autoescape(['svg'])
)
@app.route('/')
def index():
    return "Poster generator"


@app.route('/generate/<id>/<template>/<file_format>')
def generate(id, template, file_format='svg'):
    event = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
    if event.status_code is 200:
        event = Event(json.loads(event.text))
    return send_file(event.make_poster(template,file_format))