import os
import subprocess


def make_pdf(input,output):
    if os.path.isfile(input):
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(['inkscape',input,'--export-pdf={}'.format(output)], stdout=devnull, stderr=subprocess.STDOUT)
    else:
        print('Input file does not exist')
        raise()