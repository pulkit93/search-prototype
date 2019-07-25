from server.connection import client, _index


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


# Get the specified range of paragraphs from a book
def get_paragraphs(book_title, start_location, end_location):

    filter = [
        {'term': {'title': book_title}},
        {'range': {'location': {'gte': start_location, 'lte': end_location}}}
    ]

    body = {
        'size': end_location - start_location,
        'sort': {'location': 'asc'},
        'query': {bool: {filter}}
    }

    return client.search(_index, body)
