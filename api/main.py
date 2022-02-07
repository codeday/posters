from datetime import datetime
import requests, json, shutil

from fastapi import FastAPI, BackgroundTasks
from jinja2 import Environment, FileSystemLoader, select_autoescape

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from generator import PosterGenerator
from tasks import run_tasks

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

run_tasks()

client = Client(transport=AIOHTTPTransport(url="https://graph.codeday.org/"), fetch_schema_from_transport=False)

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
  
QUERY = gql(
    """
    query GetClearEvent($name: String!, $date: ClearDateTime!) {
      clear {
        findFirstEvent(where:{contentfulWebname:{equals:$name},startDate:{gte:$date}}) {
          region_name: name
          webname: contentfulWebname
          starts_at: startDate
          id
          venue {
            name
            city
            state
            line_1: addressLine1
            postal: zipCode
          }
        }
      }
    }
  """
  )

@app.get("/render/{id}/{template}/{file_format}")
async def generate(id, template, file_format='svg', promo=None, promoFor=None):
  try:
    result = await client.execute_async(QUERY, variable_values={"name": id, "date": (datetime.now()).isoformat()})
    if result["clear"]["findFirstEvent"]["venue"]:
        result["clear"]["findFirstEvent"]["venue"]["address"] = {
            "line_1": result["clear"]["findFirstEvent"]["venue"]["line_1"], "postal": result["clear"]["findFirstEvent"]["venue"]["postal"], "state": result["clear"]["findFirstEvent"]["venue"]["state"], "city": result["clear"]["findFirstEvent"]["venue"]["city"]}
    eventJson = {"current_event": result["clear"]["findFirstEvent"]}
  except Exception as e:
    print(e)
    return e

  return PosterGenerator(eventJson, promo, promoFor).make_poster('{}.svg'.format(template),file_format)

@app.get('/render_all/{id}')
async def generate_all(id, promo=None, promoFor=None):
  try:
    result = await client.execute_async(QUERY, variable_values={"name": id, "date": (datetime.now()).isoformat()})
    eventJson = {"current_event": result["clear"]["findFirstEvent"]}
  except Exception as e:
    print(e)
    return e

  PosterGenerator(eventJson, promo, promoFor).make_posters(env.list_templates())

  return FileResponse(shutil.make_archive('zip/{}'.format(id), 'zip', 'generated/{}'.format(eventJson.current_event['id'])), filename='{}.zip'.format(id))

@app.get('/api/list-templates', response_class=HTMLResponse)
def listTemplates():
  return JSONResponse([t.replace('.svg', '') for t in env.list_templates()])
