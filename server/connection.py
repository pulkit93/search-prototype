
import os
from elasticsearch import Elasticsearch

# Core ES variables for this project
INDEX = 'library'
TYPE = 'novel'
PORT = 9200
HOST = os.getenv('ES_HOST', 'localhost')


def es_client():
    """

    :return: elasticsearch client
    """
    return Elasticsearch([HOST], port=PORT)


def check_connection():
    """
    * Check connection to elasticsearch
    :return:
    """

    is_connected = False

    while not is_connected:

        print('Connecting to ES')

        try:

            health = es_client().cluster.health()
            print(health)
            is_connected = True

        except Exception as err:

            print('Connection Failed, Retrying...', err)


def reset_index():
    """
    * Clear the index, recreate it, and add mappings
    :return:
    """
    if es_client().indices.exists(INDEX):
        es_client().indices.delete(INDEX)

    es_client().indices.create(INDEX)
    _put_book_mapping()


def _put_book_mapping():
    """
    * Add book section schema mapping to ES
    :return:
    """
    schema = {
        'title': {'type': 'keyword'},
        'author': {'type': 'keyword'},
        'location': {'type': 'integer'},
        'text': {'type': 'text'}
    }

    body = {'properties': schema}

    es_client().indices.put_mapping(index=INDEX, doc_type=TYPE, body=body)
