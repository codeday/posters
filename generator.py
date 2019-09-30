import json
import os
from jinja2 import Template
import datetime,pytz
import requests


templateDir = 'templates/'
templates = []
for file in os.listdir(templateDir):
    with open(templateDir + file) as f:
        templates.append((Template(f.read()),file))
def poster(id):
        codeDay = json.loads(requests.get('https://clear.codeday.org/api/region/{}'.format(id)).text)
        if codeDay['current_event']:
            start = datetime.datetime.fromtimestamp(codeDay['current_event']['starts_at']).astimezone(pytz.timezone(codeDay['timezone']))
            if not os.path.exists('generated/{}'.format(id)):
                os.mkdir('generated/{}'.format(id))
            for t in templates:
                template = t[0]
                file = t[1]
                with open("generated/{}/{}".format(id,file), "w+") as f:
                    f.write(template.render(url=codeDay['id'],month=start.strftime('%B'),day=start.day,name=codeDay['name']))


for region in json.loads(requests.get('https://clear.codeday.org/api/regions').text):
    print('Generating poster for region {}'.format(region['name']))
    poster(region['id'])