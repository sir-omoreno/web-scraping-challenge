from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    mars_data = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():

    mars_dict = mongo.db.mars_data

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_data, upsert=True)


    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

