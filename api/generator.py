import datetime, pytz, os, subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape

from starlette.responses import RedirectResponse, FileResponse

env = Environment(
  loader= FileSystemLoader('./remote/templates/template'),
  autoescape=select_autoescape(['svg'])
)

class PosterGenerator:
  def __init__(self, data, promo=None, promoFor=None):
    self.supported_formats = ['svg', 'pdf', 'png']
    self.promo = promo
    self.promoFor = promoFor

    self.data = data
    for key in data:
      setattr(self,key,data[key])

    if self.current_event:
      self.start = datetime.datetime.fromtimestamp(data['current_event']['starts_at']).astimezone(pytz.timezone(self.timezone))
      self.month = self.start.strftime('%B')
      self.short_month = self.start.strftime('%b')
      self.day = self.start.day
      self.year = self.start.strftime('%Y')
      self.webname = self.current_event['webname']
      self.url = self.current_event['webname']

  def get_cache(self, file_format, template_name='', full=True):
    basedir = os.path.dirname(os.path.realpath(__file__)) if full else ''
    return '{}/generated/{}/{}/{}_{}_{}'.format(basedir, self.current_event['id'], file_format, self.promo, self.promoFor, template_name.replace('svg', file_format))

  def make_poster(self, template_name, file_format):
    file_format = file_format.lower()
    if file_format not in self.supported_formats:
      return('ERROR: File provided not supported format')

    if template_name not in env.list_templates():
      return({
        "requested_template": template_name,
        "template_list": env.list_templates(),
        "ERROR": 'Template provided not loaded in environment'
      })

    if not hasattr(self, 'make_poster_{}'.format(file_format)):
      return('ERROR: no make_poster method for format')

    if not self.current_event:
      return('ERROR: Event not live in Clear')

    if not os.path.isfile(self.get_cache(file_format, template_name)):
      os.makedirs(self.get_cache(file_format), exist_ok=True)
      getattr(self, 'make_poster_{}'.format(file_format))(template_name)

    return FileResponse(path=self.get_cache(file_format, template_name))

  def require_format(self, template_name, file_format):
    if not os.path.isfile(self.get_cache(file_format, template_name)):
      self.make_poster(template_name, file_format)

  def make_poster_svg(self, template_name):
    template = env.get_template(template_name)

    with open(self.get_cache('svg', template_name), "w+") as f:
      f.write(template.render(**vars(self)))

  def make_poster_pdf(self, template_name):
    self.require_format(template_name, 'svg')
    f_in = self.get_cache('svg', template_name)
    f_out = self.get_cache('pdf', template_name)

    with open(os.devnull, 'wb') as devnull:
      subprocess.check_call(['inkscape', '-z', '-f', f_in, '-A', f_out], stdout=devnull, stderr=subprocess.STDOUT)

  def make_poster_png(self, template_name):
    self.require_format(template_name, 'svg')
    f_in = self.get_cache('svg', template_name)
    f_out = self.get_cache('png', template_name)

    with open(os.devnull, 'wb') as devnull:
      subprocess.check_call(['inkscape', '-z', '-w', '600', '-f', f_in, '-e', f_out], stdout=devnull, stderr=subprocess.STDOUT)

  def make_posters(self,templates=env.list_templates()):
    for template_name in templates:
      for file_format in self.supported_formats:
        self.make_poster(template_name, file_format)
