from server.connection import client, _index, _type


# Query ES index for the provided term
def query_term(term, offset=0):
    body = {
        'from': offset,
        'query': {
            'match': {
                'text': {
                    'query': term,
                    'operator': 'and',
                    'fuzziness': 'auto'
                }
            }
        },
        'highlight': {
            'fields': {
                'text': {
                }
            }
        }
    }

    return client.search(_index, body)
