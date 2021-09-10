from flask import render_template, Response, request, jsonify, Flask
from werkzeug.exceptions import NotAcceptable
from datetime import datetime
from quotes import quotes
import random

ACCEPT_ALLOWED = ['application/json', 'text/html', 'text/plain']
TS = "timestamp"
MOTD = "motd"

def html(content): 
   return '<html><head><title>MOTD</title></head><body>' + content + '</body></html>'

def accepts(*content_types):
    def decorated(fn): 
        def wrapper(*args, **kwargs):
            requested = set(request.accept_mimetypes.values())
            defined = set(content_types)
            if len(requested & defined) == 0:
                raise NotAcceptable()
            return fn(*args, **kwargs)
        return wrapper
    return decorated

app = Flask(__name__)

def _get_motd_text(request, expired):
    motd = random.choice(quotes)["quote"] if expired else request.cookies.get(MOTD) 
    return motd

def _is_motd_expired(request, time):
    time_cookie = request.cookies.get(TS) if TS in request.cookies else None
    return time != time_cookie


@accepts(*ACCEPT_ALLOWED)
@app.route('/motd')
def motd():  
    content_type = request.accept_mimetypes.best_match(ACCEPT_ALLOWED) 

    time = datetime.utcnow().date().strftime("%m/%d/%Y") 
    expired = _is_motd_expired(request, time)
    motd_text = _get_motd_text(request, expired)

    if content_type == 'application/json':
        response = jsonify(motd_text)
    elif content_type == 'text/html':
        response = Response(html(motd_text), mimetype='text/html')
    else:
        response = Response(motd_text, mimetype='text/plain') 

    if expired: 
        response.set_cookie(TS, time, max_age=60*60*24)
        response.set_cookie(MOTD, motd_text, max_age=60*60*24)
    return response 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)