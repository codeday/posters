from flask import send_file
from jinja2 import Environment, FileSystemLoader, select_autoescape
from event import Event
import requests, json, shutil
from templates import app
app = Flask('posters')
env = Environment(
    loader= FileSystemLoader('./posterTemplates'),
    autoescape=select_autoescape(['svg'])
)
@app.route('/')
def index():
    return "Poster generator"

@app.route('')
@app.route('/generate/<id>/<template>/<file_format>')
def generate(id, template, file_format='svg'):
    event = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
    if event.status_code is 200:
        event = Event(json.loads(event.text))
    else:
        return "No event found with id {}".format(id),404
    return send_file(event.make_poster(template + '.svg', file_format))


@app.route('/generate_all/<id>')
def generate_all(id):
    event = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
    if event.status_code is 200:
        event = Event(json.loads(event.text))
    else:
        return "No event found with id {}".format(id),404
    event.make_posters()

    return send_file(shutil.make_archive('zip/{}'.format(id), 'zip', 'generated/{}'.format(id)))


@app.route('/listTemplates')
def list_templates():
    return json.dumps([t.replace('.svg', '') for t in env.list_templates()])
