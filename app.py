# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:07:22 2019

@author: xiang
"""
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
 
    db=mongo.db.mars_db.find_one()
  # Return template and data
    return render_template("index.html", mars = mars)
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    db = mongo.db.mars_db
    mars = scrape_mars.scrape()
    mongo.db.collection.update({},mars,upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    #scrape()
    print("a")

