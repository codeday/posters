import requests, json, shutil

from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader, select_autoescape

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles

from generator import PosterGenerator

env = Environment(
  loader= FileSystemLoader('./posterTemplates'),
  autoescape=select_autoescape(['svg'])
)

app = FastAPI()

app.mount("/generated", StaticFiles(directory="generated"), name="generated")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get('/')
def root():
  return "Poster Generator API"

@app.get("/api/generate/{id}/{template}/{file_format}")
def generate(id, template, file_format='svg'):
  eventRequest = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
  try:
    eventJson = json.loads(eventRequest.text)
  except:
    return "No event found with id {}".format(id),404
  return PosterGenerator(eventJson).make_poster('{}.svg'.format(template),file_format)

@app.get('/api/generate_all/{id}')
def generate_all(id):
  eventRequest = requests.get('https://clear.codeday.org/api/region/{}'.format(id))
  try:
    eventJson = json.loads(eventRequest.text)
  except:
    return "No event found with id {}".format(id),404
  PosterGenerator(eventJson).make_posters(env.list_templates())

  return FileResponse(shutil.make_archive('zip/{}'.format(id), 'zip', 'generated/{}'.format(id)), filename='{}.zip'.format(id))

@app.get('/api/listTemplates/', response_class=HTMLResponse)
def listTemplates():
  return json.dumps([t.replace('.svg', '') for t in env.list_templates()])