
import os
from elasticsearch import Elasticsearch

# Core ES variables for this project
_index = 'library'
_type = 'novel'
_port = 9200
_host = os.getenv('ES_HOST', 'localhost')

client = Elasticsearch([_host], port=_port)


def check_connection():

    is_connected = False

    while not is_connected:

        print('Connecting to ES')

        try:

            health = client.cluster.health()
            print(health)
            is_connected = True

        except Exception as err:

            print('Connection Failed, Retrying...', err)


# Clear the index, recreate it, and add mappings
def reset_index():

    if client.indices.exists(_index):
        client.indices.delete(_index)

    client.indices.create(_index)
    _put_book_mapping()


# Add book section schema mapping to ES
def _put_book_mapping():
    schema = {
        'title': {'type': 'keyword'},
        'author': {'type': 'keyword'},
        'location': {'type': 'integer'},
        'text': {'type': 'text'}
    }

    body = {'properties': schema}

    return client.indices.put_mapping(index=_index, doc_type=_type, body=body)
