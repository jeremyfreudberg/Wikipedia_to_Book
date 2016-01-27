from flask import Flask
import wikipedia
from process_urls import *

app = Flask(__name__)
@app.route('/<term>')
def page(term):
    w = wikipedia.page(term)
    ref =w.references
    gbooks = [x for x in ref if 'books.google' in x]
    processed = [process_gbooks(y) for y in gbooks]
    if len(processed) > 0:
        return str(processed)
    else:
        return 'No google books found. :('

if __name__ == '__main__':
    app.run(debug=True)
        
