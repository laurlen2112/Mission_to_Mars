from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

#10.5.1

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#set app route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#adding the route and function
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {'$set':mars_data}, upsert = True)
    return redirect ('/', code = 302)

#now that we have gathered data we are updating the database using updateOne
#.update_one(query_parameter, {'$set': data}, options)

if __name__ == "__main__":
   app.run(debug = True)
