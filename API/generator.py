import datetime, pytz, os
from jinja2 import Environment, FileSystemLoader, select_autoescape

from starlette.responses import RedirectResponse

env = Environment(
    loader= FileSystemLoader('./posterTemplates'),
    autoescape=select_autoescape(['svg'])
)

class PosterGenerator:
  def __init__(self,data):
    for key in data:
      setattr(self,key,data[key])
    if self.current_event:
      self.start = datetime.datetime.fromtimestamp(data['current_event']['starts_at']).astimezone(pytz.timezone(self.timezone))
      self.month = self.start.strftime('%B')
      self.short_month = self.start.strftime('%b')
      self.day = self.start.day
      self.year = self.start.strftime('%Y')
    self.data = data

  def make_poster(self, template, file_format):
    supported_files = ['svg','pdf']
    file_format = file_format.lower()
    if file_format not in supported_files:
        return('ERROR: File provided not supported format')
    if template not in env.list_templates():
        return({
          "requested_template": template, 
          "template_list": env.list_templates(), 
          "ERROR": 'Template provided not loaded in environment'
        })
    if not self.current_event:
        return('ERROR: Event not live in Clear')
    file = template
    template = env.get_template(file)
    id = self.id
    if not os.path.exists('generated/'):
        os.mkdir('generated/')
    if not os.path.exists('generated/{}/'.format(id)):
        os.mkdir('generated/{}/'.format(id))
    if not os.path.exists('generated/{}/svg/'.format(id)):
        os.mkdir('generated/{}/svg/'.format(id))
    if not os.path.exists('generated/{}/pdf/'.format(id)):
        os.mkdir('generated/{}/pdf/'.format(id))
    with open("generated/{}/svg/{}".format(id, file), "w+") as f:
        f.write(template.render(**vars(self)))
    # if file_format == 'pdf':
    #     make_pdf('generated/{}/svg/{}'.format(id, file),
    #               'generated/{}/pdf/{}'.format(id, file.replace('.svg', '.pdf')))
    #     return 'generated/{}/pdf/{}'.format(id, file.replace('.svg', '.pdf'))
    return RedirectResponse(url='/generated/{}/svg/{}'.format(id, file))

  def make_posters(self,templates=env.list_templates()):
    for template in templates:
      self.make_poster(template, 'svg')  # pdf so it makes them both

  # def make_pdf(input,output):
  #     if os.path.isfile(input):
  #         with open(os.devnull, 'wb') as devnull:
  #             subprocess.check_call(['inkscape {} --export-pdf={}'.format(input, output)], stdout=devnull, stderr=subprocess.STDOUT)
  #     else:
  #         print('Input file does not exist')
  #         return