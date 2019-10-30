import svgwrite
import random
import requests
import json
from event import Event

def poster(filename, name,details):
    dwg = svgwrite.Drawing(filename,size=('9in','14in'))
    dwg.add(dwg.rect(size=('100%','100%'),fill='#ff686b'))
    dwg.add(dwg.image(href='srnd.svg',insert=('2%','1%'),width='8%'))
    dwg.embed_stylesheet("""
        @import url('https://srnd-cdn.net/fonts/avenir-next/minimal.css');
        .avenir {
            font-family: "Avenir Next";
        }
        """)
    header = dwg.add(dwg.g(class_="avenir", ))
    header.add(dwg.text('CodeDay {}'.format(name), text_anchor='middle', font_size='5em',insert=('50%','12%'),fill='#ffffff'))
    paragraph = dwg.add(dwg.g(class_="avenir", ))
    paragraph.add(dwg.text(details, text_anchor='middle', font_size='3em', fill='#ffffff',
                     insert=('50%', '19%')))
    paragraph.add(dwg.text('Noon-Noon', text_anchor='middle', font_size='3em', fill='#ffffff',
                     insert=('50%', '23%')))
    dwg.save()


def suffix(d): # https://stackoverflow.com/a/5891598/4991969
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


codeDays = json.loads(requests.get('https://clear.codeday.org/api/regions').text)
codeDay = Event(random.choice([day for day in codeDays if day['current_event']]))
poster('codeDay.svg',codeDay)