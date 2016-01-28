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
    #result = 'Append the title of a Wikipedia article to this URL\nNeed an example? Try <a href="/Potato">Potato</a>
    result = []
    return render_template('pretty.html',result=result)
    
@app.route('/<term>')
def page(term):
    try:
        w = wikipedia.page(term)
    except wikipedia.exceptions.DisambiguationError:
        return render_template('pretty.html',result='Disambiguaton Error')
    except wikipedia.exceptions.PageError:
        return render_template('pretty.html',result='Article not found')
    ref =w.references
    gbooks = [x for x in ref if 'books.google' in x]
    processed = [process_gbooks(y) for y in gbooks]
    if len(processed) > 0:
        result = str(processed)
    else:
        result = 'No google books found. :('
    return render_template('pretty.html',result=result)

if __name__ == '__main__':
    app.run(debug=True)
        
