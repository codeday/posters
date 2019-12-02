import datetime, pytz, os
from make_pdf import make_pdf
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader= FileSystemLoader('./templates'),
    autoescape=select_autoescape(['svg'])
)


class Event:
    def __init__(self,data):
        self.current_event = None
        for key in data:
            setattr(self,key,data[key])
        self.data = data
        if self.current_event:
            self.start = datetime.datetime.fromtimestamp(data['current_event']['starts_at']).astimezone(pytz.timezone(self.timezone))
            self.month = self.start.strftime('%B')
            self.short_month = self.start.strftime('%b')
            self.day = self.start.day
            self.year = self.start.strftime('%Y')
        self.url = self.id

    def make_poster(self,template, file_format):
        supported_files = ['svg','pdf']
        file_format = file_format.lower()
        if file_format not in supported_files:
            print('ERROR: File provided not supported format')
            raise
        if template not in env.list_templates():
            print('ERROR: Template provided not loaded in environment')
            raise
        if not self.current_event:
            print('ERROR: Event not live in Clear')
            raise
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
        if file_format == 'pdf':
            make_pdf('generated/{}/svg/{}'.format(id, file),
                     'generated/{}/pdf/{}'.format(id, file.replace('.svg', '.pdf')))
            return 'generated/{}/pdf/{}'.format(id, file.replace('.svg', '.pdf'))
        return 'generated/{}/svg/{}'.format(id, file)

    def make_posters(self,templates=env.list_templates()):
        for template in templates:
            self.make_poster(template, 'pdf')  # pdf so it makes them both
