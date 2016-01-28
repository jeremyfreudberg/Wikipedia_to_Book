from flask import Flask
from flask import render_template
from flask.ext.bootstrap import Bootstrap
import wikipedia
from process_urls import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def notfound(e):
    return render_template('error.html',num=404),404

@app.errorhandler(500)
def internal(e):
    return render_template('error.html',num=500),500

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html',num=403),403

@app.route('/')
def index():
    result = ''
    msg = "Append the title of a Wikipedia article to this URL (form coming soon).<br>"
    msg += 'Need a good example? Not all articles are created equal. Try <a href="/Potato">Potato</a>.'
    return render_template('pretty.html',result=result, msg=msg)
    
@app.route('/<term>')
def page(term):
    try:
        w = wikipedia.page(term)
    except wikipedia.exceptions.DisambiguationError:
        return render_template('pretty.html',result='', msg='Disambiguation Error')
    except wikipedia.exceptions.PageError:
        return render_template('pretty.html',result='', msg='Article not found')
    ref =w.references
    gbooks = [x for x in ref if 'books.google' in x]
    processed = [process_gbooks(y) for y in gbooks]
    while ('Timeout',) in processed:
        processed.remove(('Timeout',))
    while ('No title found', 'No author found', 'No ISBN found') in processed:
        processed.remove(('No title found', 'No author found', 'No ISBN found'))
    if len(processed) > 0:
        result = processed
    else:
        result = ['No google books found. :(']
    return render_template('pretty.html',result=result, msg=None)

if __name__ == '__main__':
    app.run(debug=True)
        
