import requests
def process_gbooks(s):
    ss = s.split('?id=')[1].split('&')[0]
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q={}'.format(ss))
    rj = r.json()
    title = rj['items'][0]['volumeInfo']['title']
    author = rj['items'][0]['volumeInfo']['authors']
    iI = rj['items'][0]['volumeInfo']['industryIdentifiers']
    for x in [0,1]: # because sometimes Google is inconsistent
        if iI[x]['type'] == 'ISBN_13':
            break
    isbn13 = iI[x]['identifier']
    return (title, author, isbn13)
