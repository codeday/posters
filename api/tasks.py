import time, threading
import os, tempfile, zipfile, shutil
from urllib import request

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

if __name__ == "__main__":
  print("Running tasks...")
  sync_templates()
  cleanup()
