from flask import Flask, render_template, request, redirect, url_for, flash, abort
import pymongo, string, random
from random import choice

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.cfjrqh5.mongodb.net/?retryWrites=true&w=majority")
db = client["test"]
items_collection = db["url"]
urls = []

app.secret_key = 'my_secret_key'

def generate(num_of_chars: int):
    return ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))
    
    
        
@app.route('/', methods=['GET', 'POST'])
def index():
    
    items = items_collection.find()
    
    if request.method == 'POST':
        url = request.form['url_get']
        custom = request.form['custom_url']
        
        if not custom:
            custom = generate(8)
            
        if custom:
            existing = items_collection.find_one({'custom_url':custom})    
            if existing is not None:
                flash('This custom id already use please try another one')
                return redirect(url_for(index))
            
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        
        s_url = request.host_url + custom
        
        items_collection.insert_one({
                "url_get": url,
                "custom_url": custom,
                "short_url" :  s_url,
        })
            
        # custom = request.host_url + custom
    
        short_url =  request.host_url + custom
        

    return render_template("home.html", items=items)


@app.route('/<custom>')
def redirect_url(custom):  
    # Find the link with the matching custom URL
    link = items_collection.find_one({'custom_url': custom})
    
    if link is not None:
        # Redirect the user to the URL stored in the 'url_get' field
        return redirect(link['url_get'])
    else:
        # Handle the case where the link was not found
        abort(404)


if __name__ == '__main__':
    app.run()