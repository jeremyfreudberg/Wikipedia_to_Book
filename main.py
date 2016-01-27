from flask import Flask
import wikipedia
import requests

def process(s):
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

app = Flask(__name__)
@app.route('/<term>')
def page(term):
    w = wikipedia.page(term)
    ref =w.references
    gbooks = [x for x in ref if 'books.google' in x]
    processed = [process(y) for y in gbooks]
    if len(processed) > 0:
        return str(processed)
    else:
        return 'No google books found. :('

app.run(debug=True)
        
