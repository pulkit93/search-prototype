import glob
import os
import re
from elasticsearch import helpers
import connection as es_connection


def parse_book_file(file_path):
    """
    * Read an individual book text file, and extract the title, author, and paragraphs
    :param file_path:
    :return:
    """
    # Read text file
    book = open(file_path, 'r', encoding='utf8')
    book_text = book.read()
    book.close()

    # Find book title and author
    title = ''.join(re.findall(r'Title:\s(.*?)\s*(?=\n\n)', book_text, re.S)[0].split('\n'))
    author_match = re.findall(r'Author:\s(.*?)\s*(?=\n)', book_text, re.S)
    author = 'Unknown Author' \
        if (not author_match or author_match[0].strip() == '') \
        else author_match[0]

    print('Reading Book - {0} By {1}'.format(title, author))

    # Find Guttenberg metadata header and footer
    start_of_book_index = [m.end(0) for m in
                           re.finditer(r'^(\*{3}\s*START OF (THIS|THE) PROJECT GUTENBERG EBOOK.+\*{3})$',
                                       book_text, re.M)][0]
    end_of_book_index = [m.start(0) for m in
                         re.finditer(r'^(\*{3}\s*END OF (THIS|THE) PROJECT GUTENBERG EBOOK.+\*{3})$',
                                     book_text, re.M)][-1]

    # Clean book text and split into array of paragraphs
    # Remove Guttenberg header and footer
    # Split each paragraph into it's own array entry
    paragraphs = book_text[start_of_book_index:end_of_book_index] \
        .split('\n\n\n\n')
    # Remove paragraph line breaks and whitespace
    # Guttenberg uses "_" to signify italics.  We'll remove it, since it makes the raw text look messy.
    paragraphs = [para.replace('\r\n', ' ').strip().replace('_', '')
                  for para in paragraphs]
    # Remove empty lines
    paragraphs = ['\n'.join([line for line in para.split('\n') if line.strip()])
                  for para in paragraphs]

    print('Parsed ' + str(len(paragraphs)) + ' Paragraphs\n')

    return title, author, paragraphs


def insert_book_data(title, author, paragraphs):
    """
    * Bulk index the book data in Elasticsearch
    :param title:
    :param author:
    :param paragraphs:
    :return:
    """
    bulk_ops = []  # Array to store bulk operations

    # Add an index operation for each section in the book
    for i in enumerate(paragraphs):
        # Describe action
        bulk_ops.append({'_index': es_connection.INDEX, '_type': es_connection.TYPE})

        # Add document
        bulk_ops[-1].update({
            'author': author,
            'title': title,
            'location': i,
            'text': paragraphs[i]
        })

    # Insert remainder of bulk ops array
    helpers.bulk(es_connection.es_client(), bulk_ops)
    print('Indexed Paragraphs {0} - {1}\n\n\n'.format(len(paragraphs) - (len(bulk_ops) / 2),
                                                      len(paragraphs)))


def read_and_insert_books():
    """
    * Clear ES index, parse and index all files from the books directory
    :return:
    """
    try:
        # Clear previous ES index
        es_connection.reset_index()

        # Read books directory
        files = glob.glob('./books/*.txt')
        print('Found {} Files'.format(len(files)))

        # Read each book file, and index each paragraph in elasticsearch
        for file in files:
            print('Reading File - {}'.format(file))
            file_path = os.path.join(file)
            title, author, paragraphs = parse_book_file(file_path)
            insert_book_data(title, author, paragraphs)

    except Exception as err:
        print(err)


read_and_insert_books()
