import requests
def process_gbooks(s):
    ss = s.split('?id=')[1].split('&')[0]
    try:
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q={}'.format(ss),timeout=1)
    except requests.exceptions.Timeout:
        return ('Timeout',)
    rj = r.json()
    try:
        title = rj['items'][0]['volumeInfo']['title']
    except KeyError:
        title = 'No title found'
    try:
        author = rj['items'][0]['volumeInfo']['authors']
    except KeyError:
        author = 'No author found'
    try:
        iI = rj['items'][0]['volumeInfo']['industryIdentifiers']
    except KeyError:
        iI = [{'type':'non-existent'}]
    isbn_index = -1
    try:
        for x in [0,1]:
            if iI[x]['type'] == 'ISBN_13':
                isbn_index = x
        isbn13 = iI[isbn_index]['identifier']
    except IndexError:  
        isbn13 = 'No ISBN found'
    return (title, author, isbn13)
