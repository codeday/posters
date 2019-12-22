import requests, json, shutil

from fastapi import FastAPI, BackgroundTasks
from jinja2 import Environment, FileSystemLoader, select_autoescape

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from generator import PosterGenerator
from tasks import run_tasks

run_tasks()

env = Environment(
  loader= FileSystemLoader('./remote/templates/template'),
  autoescape=select_autoescape(['svg'])
)

app = FastAPI()

app.mount("/preview", StaticFiles(directory="./preview"), name="preview")
app.mount("/static", StaticFiles(directory="./build/static"), name="static")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

@app.get('/')
def root():
  return HTMLResponse(file_get_contents("./build/index.html"))

@app.get('/sync')
def sync(background_tasks: BackgroundTasks):
  background_tasks.add_task(run_tasks)
  return HTMLResponse('ok')

@app.get("/render/{id}/{template}/{file_format}")
def generate(id, template, file_format='svg', promo=None, promoFor=None):
  eventRequest = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
  try:
    eventJson = json.loads(eventRequest.text)
  except:
    return "No event found with id {}".format(id),404

  return PosterGenerator(eventJson, promo, promoFor).make_poster('{}.svg'.format(template),file_format)

@app.get('/render_all/{id}')
def generate_all(id, promo=None):
  eventRequest = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
  try:
    eventJson = json.loads(eventRequest.text)
  except:
    return "No event found with id {}".format(id),404
  PosterGenerator(eventJson, promo, promoFor).make_posters(env.list_templates())

  return FileResponse(shutil.make_archive('zip/{}'.format(id), 'zip', 'generated/{}'.format(eventJson.current_event['id'])), filename='{}.zip'.format(id))

@app.get('/api/list-templates', response_class=HTMLResponse)
def listTemplates():
  return JSONResponse([t.replace('.svg', '') for t in env.list_templates()])
