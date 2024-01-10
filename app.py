from flask import Flask, render_template, g

import csv
import os
import googlemaps
import sqlite3

# Initialize Flask App
app = Flask(__name__)
# This "signs the session's cookies"
app.secret_key = os.urandom(24) 

# Set variable for API key in a local environment
api_key = os.getenv('API_KEY')

# Initialize Googlemaps with API key (for using zip code to place markers on the map)
gmaps = googlemaps.Client(key=api_key)

# Create a SQLite3 database from an existing CSV file
# get_database is a function that uses Python's getattr to return a variable independently accessible between requests
# If the dataase is empty, the function creates the db variable using alumni.db
def get_database():
    db = getattr(g, 'database', None)
    if db is None:
        db = g.database = sqlite3.connect("alumni.db")

        cursor = db.cursor()

        # Check if the 'alumni' table is empty
        cursor.execute("SELECT count(*) FROM alumni")
        count = cursor.fetchone()[0]
        
        if count == 0:

            # If the table is empty, insert data from the CSV file
            with open("mpra_alumni.csv") as file:
                alumni_file = csv.DictReader(file)

                # iterate through each row in alumni_file (list of dictionaries)
                for row in alumni_file:

                    # Input all of the spreadsheet data into a table in the alumni.db file (cursor)
                    cursor.execute("INSERT INTO alumni (year, last, first, address, city, state, zip, email, alt_email, cell, home, employer, emp_address, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (row['Class Year'], row['Last Name'], row['First Name'], row["Address"], row["City"], row["State"], row["Zip"], row["Preferred Email"], row["Alternate Email"], row["Cell Phone Number"], row["Home Number"], row["Current Employer"], row["Employer Address"], row["Last Updated"]))

            # Retrieve the entries with a zip code, returning primary key
            cursor.execute("SELECT id, zip FROM alumni WHERE zip IS NOT NULL and zip != '';")

            # Put the data retrieved into a list of tuples via fetchall
            alumni_list_of_tuples = cursor.fetchall()

            # Change the zip to lattitude and longitude to be put in a sql table
            for entries in alumni_list_of_tuples:
                zip_code = entries[1]
                geocode_result = gmaps.geocode(zip_code)
                if geocode_result:
                    latitude = geocode_result[0]["geometry"]["location"]["lat"]
                    longitude = geocode_result[0]["geometry"]["location"]["lng"]
                    # Put all of this data into a SQL table to access in the html page
                    cursor.execute("INSERT INTO latlong (alumni_id, lat, lng) VALUES (?, ?, ?)", (entries[0], latitude, longitude))
        db.commit()
    return db
    
# Flask decorator that allows the access_database function to run at the opening of each request, e.g. @app.route
@app.before_request
# Accesses the database with a "g" object, specific to each request, not interfering with concurrent requests
def access_database():
    g.db = get_database()

# Flask decorator that allows the close_database function to run at the end of each request
@app.teardown_request
# Checks if there is a database connection to the "g" object and closes access so as not to interfere with concurrent requests
def close_database(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Index Page
@app.route('/', methods=['GET'])
def index():

    # Variable for temporary database access
    cursor = g.db.cursor()

    # Create a list of tuples to pass to jinja
    cursor.execute("SELECT first, last, year, lat, lng FROM alumni JOIN latlong ON alumni.id = latlong.alumni_id;")
    list_of_tuples = cursor.fetchall()

    return render_template('index.html', list=list_of_tuples)

# Alumni Page
@app.route('/alumni', methods=['GET'])
def alumni():
        
        cursor = g.db.cursor()
        
        cursor.execute("SELECT first, last, year, city, state, employer FROM alumni JOIN latlong ON alumni.id = latlong.alumni_id;")
        alumni_tuples = cursor.fetchall()

        return render_template("alumni.html", alumni=alumni_tuples)

# Running the Flask App
if __name__ == '__main__':
    app.run(debug=False)  # Set debug to False in production
    