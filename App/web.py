import os
import os.path
import functools
import time
import datetime
import logging

from bottle import Bottle, request, run, jinja2_view, redirect, abort, static_file, Jinja2Template

from .common import app_config
from .models import UrlShorten

logger = logging.getLogger(__name__)

def format_datetime(value, format_str="%Y-%-m-%d %H:%M:%S"):
    if not value: return "n/a"
    dt = datetime.datetime.fromtimestamp(value)
    return dt.strftime(format_str)


Jinja2Template.settings = {
    "filters":{'datetime': format_datetime},
}

templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
view = functools.partial(jinja2_view, template_lookup=[templates_dir])
application = app = Bottle()

@app.route('/assets/<path:path>')
def assets(path):
    return static_file(path, root=os.path.join(app_config.base_dir, 'public/assets'))

@app.get('/ping')
def ping():
    return 'pong@'+str(time.time())

@app.post('/shorten')
def shorten():
    logger.debug("got %r", request.json)
    item = UrlShorten.generate_and_save(request.json['longUrl'])
    return {
        "shorten":item.short,
        "link": item.url,
    }

@app.get('/')
@view('index.html')
def index():
    return {}

@app.post('/')
def web_shorten():
    url = request.POST.get('longUrl')
    logger.debug("got %r", url)
    item = UrlShorten.generate_and_save(url)
    code = item.code
    redirect("/"+code+"+")

@app.get(r'/<code:re:[a-zA-Z0-9_\-]+>+')
@view('index.html')
def report(code):
    logger.debug('got code=%r', code)
    item = UrlShorten.find_by_code(code)
    if not item: abort(404, "No such code")
    logger.debug('Code=%(code)r visited. Real URL: %(url)r', code=code, url=item.url)
    return {"item":item}

@app.get(r'/<code:re:[a-zA-Z0-9_\-]+>')
def visit(code):
    logger.debug('Code [%r]', code)
    item = UrlShorten.find_and_increment(code)
    if not item: return redirect('http://bit.ly/'+code, code=301)
    logger.debug('Code=%(code)r visited. Real URL: %(url)r', code=code, url=item.url)
    return redirect(item.url, code=301)


def main():
    run(app, host='localhost', port=8800, debug=True)

if __name__ == '__main__':
    main()
