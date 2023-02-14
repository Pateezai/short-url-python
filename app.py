from flask import Flask, render_template, request
import asyncio
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.cfjrqh5.mongodb.net/?retryWrites=true&w=majority")
db = client["url_db"]
items_collection = db["urls"]
urls = []

@app.route('/', methods=['GET', 'POST'])
async def items():
        if request.method == 'POST':
            # Get the item name and value from the request form
            url = request.form['url_get']
            custom = request.form['custom_url']

            # Insert the new item into the "items" collection
            items_collection.insert_one({
                "url_get": url,
                "custom_url": custom,
            })
            return render_template("index.html", urls=urls)
        else:
            # Find all documents in the "items" collection
            items = items_collection.find()
            
            for item in items:
                urls.append((item['url_get'], item['custom_url']))
            
            return render_template("index.html", urls=urls)


if __name__ == '__main__':
    app.run(port=6000)
    # app.run(port=6000)