import time, threading
import os, tempfile, zipfile, shutil
from urllib import request
from generator import PosterGenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

def sync_templates():
  zip_path = os.path.join(tempfile.mkdtemp(), 'templates.zip')
  request.urlretrieve("https://github.com/srnd/CodeDayPosterTemplates/archive/master.zip", zip_path)

  os.makedirs('remote/templates_new')
  with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('remote/')
    os.rename('remote/CodeDayPosterTemplates-master', 'remote/templates_new')

  try:
    os.rename('remote/templates', 'remote/templates_old')
  except:
    pass

  os.rename('remote/templates_new', 'remote/templates')
  shutil.rmtree('remote/templates_old', ignore_errors=True)
  os.remove(zip_path)


  # Generate samples
  env = Environment(
    loader= FileSystemLoader('./remote/templates/template'),
    autoescape=select_autoescape(['svg'])
  )

  with open('example.json', 'r') as exFile:
    data=json.loads(exFile.read())

  shutil.rmtree('generated/example', ignore_errors=True)
  PosterGenerator(data, 'PROMO', '20% off').make_posters(env.list_templates())
  shutil.rmtree('preview', ignore_errors=True)
  os.rename('generated/example/png', 'preview')
  shutil.rmtree('generated/example', ignore_errors=True)
  for f in os.listdir('preview'):
    os.rename('preview/{}'.format(f), 'preview/{}'.format(f[str.index(f, '_')+1:]));


def cleanup():
  for dir in ('generated', 'zip'):
    if (os.path.exists(dir)):
      for subdir in os.listdir(dir):
        path = os.path.realpath(os.path.join(dir, subdir))
        if (os.path.basename(path) != '.gitkeep'):
          if (os.path.isdir(path)):
            shutil.rmtree(path)
          else:
            os.remove(path)

def run_tasks():
  sync_templates()
  cleanup()


if __name__ == "__main__":
  print("Running tasks...")
  run_tasks()
