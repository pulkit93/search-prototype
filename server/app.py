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


def _validate_search(term, offset):

    if term and isinstance(term, str) and len(term) <= 60:
        if isinstance(offset, int) and offset >= 0:
            return None

    return BadRequest()


def _validate_paragraphs(book_title, start, end):

    if book_title and isinstance(book_title, str) and len(book_title) <= 256:
        if isinstance(start, int) and start >= 0:
            if isinstance(end, int) and end > start:
                return None

    return BadRequest()


@app.route('/search', methods=['GET'])
def search():
    """
    * GET /search
    * Search for a term in the libraryDefault route to return a simple message
    * Query Params -
    *   term: string under 60 characters
    *   offset: positive integer
    """
    term = request.args.get('term', None)
    offset = request.args.get('offset', 0)
    _raise_if(_validate_search(term, int(offset)))
    return es_search.query_term(term, int(offset))


@app.route('/paragraphs', methods=['GET'])
def paragraphs():
    """"
    * GET /paragraphs
    * Get a range of paragraphs from the specified book
    * Query Params -
    *   book_title: string under 256 characters
    *   start: positive integer
    *   end: positive integer greater than start
    :return:
    """
    book_title = request.args.get('bookTitle', None)
    start = request.args.get('start', 0)
    end = request.args.get('end', 10)
    _raise_if(_validate_paragraphs(book_title, int(start), int(end)))
    return es_search.get_paragraphs(book_title, int(start), int(end))


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method,
                     request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(err):
    trace_back = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr,
                     request.method, request.scheme, request.full_path, trace_back)
    return err


if __name__ == '__main__':

    try:
        handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
        port = os.getenv('PORT', 3000)
        host = os.getenv('HOST', '127.0.0.1')
        logger = logging.getLogger('tdm')
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)
        app.run(host, port)
    except Exception as exc:
        print(exc)
