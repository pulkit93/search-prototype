import os
import logging
import traceback
from logging.handlers import RotatingFileHandler
from time import strftime
from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

import server.search as es_search

app = Flask(__name__)
CORS(app)


def _raise_if(exc):
    if exc is not None:
        raise exc


def _validate(term, offset):

        if term and isinstance(term, str) and len(term) <= 60:
            if isinstance(offset, int) and offset >= 0:
                return None

        return BadRequest()


@app.route('/search', methods=['GET'])
def search():
    """
    GET /search
    Search for a term in the libraryDefault route to return a simple message
    """
    term = request.args.get('term', None)
    offset = request.args.get('offset', 0)
    _raise_if(_validate(term, offset))
    return es_search.query_term(term, offset)


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(err):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return err


if __name__ == '__main__':

    try:
        handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
        port = os.getenv('PORT', 3000)
        logger = logging.getLogger('tdm')
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)
        app.run('0.0.0.0', port)
    except Exception as e:
        print(e)
