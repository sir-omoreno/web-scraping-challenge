from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    data = mongo.db.data.find_one()
    # Return template and data
    return render_template("/templates/index.html", mars=data)

if __name__ == "__main__":
    app.run(debug=True)