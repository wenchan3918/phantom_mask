# python manage.py test_push_task
import json


def choice2html(choices):
    return json.dumps(dict(choices), indent=4, ensure_ascii=False).replace(' ', '&nbsp;').replace('\n', '<br>')


def dict2html(objects):
    return json.dumps(objects, indent=4, ensure_ascii=False).replace(' ', '&nbsp;').replace('\n', '<br>')

def text2hmtl(text):
    return text.replace(' ', '').replace('\n', '<br>')
def choice2str(choices):
    return str(dict(choices))
