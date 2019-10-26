import json
import os
from jinja2 import Template
import datetime,pytz
import requests
from make_pdf import make_pdf

templateDir = 'templates/'
templates = []
for file in os.listdir(templateDir):
    with open(templateDir + file) as f:
        templates.append((Template(f.read()),file))


def poster(id):
        codeDay = json.loads(requests.get('https://clear.codeday.org/api/region/{}'.format(id)).text)
        if codeDay['current_event']:
            start = datetime.datetime.fromtimestamp(codeDay['current_event']['starts_at']).astimezone(pytz.timezone(codeDay['timezone']))
            if not os.path.exists('generated/'):
                os.mkdir('generated/')
            if not os.path.exists('generated/{}/'.format(id)):
                os.mkdir('generated/{}/'.format(id))
            if not os.path.exists('generated/{}/svg/'.format(id)):
                os.mkdir('generated/{}/svg/'.format(id))
            if not os.path.exists('generated/{}/pdf/'.format(id)):
                os.mkdir('generated/{}/pdf/'.format(id))
            for t in templates:
                template = t[0]
                file = t[1]
                with open("generated/{}/svg/{}".format(id,file), "w+") as f:
                    f.write(template.render(url=codeDay['id'],short_month=start.strftime('%b'),month=start.strftime('%B'),day=start.day,name=codeDay['name']))
                make_pdf('generated/{}/svg/{}'.format(id,file),'generated/{}/pdf/{}'.format(id,file.replace('.svg','.pdf')))


for region in json.loads(requests.get('https://clear.codeday.org/api/regions').text):
    print('Generating posters for region {}'.format(region['name']))
    poster(region['id'])

