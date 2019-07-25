from server.connection import es_client, INDEX


def query_term(term, offset=0):
    """
    * Query ES index for the provided term
    :param term:
    :param offset:
    :return:
    """
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

    return es_client().search(INDEX, body)


def get_paragraphs(book_title, start_location, end_location):
    """
    * Get the specified range of paragraphs from a book
    :param book_title:
    :param start_location:
    :param end_location:
    :return:
    """

    search_filter = [
        {'term': {'title': book_title}},
        {'range': {'location': {'gte': start_location, 'lte': end_location}}}
    ]

    body = {
        'size': end_location - start_location,
        'sort': {'location': 'asc'},
        'query': {'bool': {'filter': search_filter}}
    }

    return es_client().search(INDEX, body)
