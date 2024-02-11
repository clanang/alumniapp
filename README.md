# Web App Title: ALUMNI

### Current Website link on gcloud: [Alumni App](https://mpra-alumni-app.ue.r.appspot.com)

#### Video Demo:  [My video](https://youtu.be/9B-TGDPOMDU?si=FWOhCXEiOdMKqudS)
Note: this video showcases a version of this app that uses a Google Spreadsheet API instead of the CSV file (as used in this app) to access the alumni information. I also displayed API keys in this video, but have since deleted those for security reasons.
#### Summary
This is a web application that takes alumni data from a CSV file and displays the information graphically via markers on a map. Each marker represents a graduate and their current location. This information serves as a visual representation for where students are living after graduation. It highlights trends and informs faculty and prospective students about cities that potentially serve our graduates. Displayed on the map are also names and graduation dates. For more detailed information, a user is able to click on the map to view a table of alumni that includes first name, last name, year of graduation, city, state, and employer/company. 

#### Geocoding Google API Key
This app uses a Google geocoding API key to translate zip codes into geographic coordinates. For users to clone and run this code, for security reasons, they will need to supply their own Google geocoding API key. Once they've obtained a key, they will simply define an environment variable in the terminal, as follows:
- Window system: set API_KEY=your_api_key_here
- Linux/Mac system: export API_KEY=your_api_key_here

#### Languages and Integration
- Googlemaps geocoding API
- Python for backend
- SQL databases for alumni tables
- Flask/Jinja, CSS, and HTML for the frontend
- JavaScript libraries

#### History
The Music Production and Recording Arts (MPRA) program at Elon University has been graduating students since 2009. The program has not formally kept track of these graduates or publicized their post-graduation progress. Keeping track of alumni is important for the program as it informs faculty about successes and challenges, in turn influencing program and curricular changes. Additionally, publicizing alumni data serves as a marketing tool for the program, informing prospective students about the success of graduates. Prospective students may also be encouraged by the robustness of an alumni network. With this in mind, this project's goal is to more formally compile alumni data and present it online. The data will be dynamic and update accordingly as information changes and new information is submitted.

 ### Implementation
 #### The Beginning
The starting point for this project was a Google Sheet document that contains a partial list of alumni. Included in this list were names, graduation dates, addresses, phone numbers, and employment information. I first crafted my Python file, importing libraries and initializing Flask.
 #### Geocoding API
Using Google's Geocoding API, I used the gmaps.geocode() method to access the latitude and longitude of each student that had associated zip code information for where they live. This information was then passed into the new "latlong" SQLite3 table, along with the alumni IDs. I then used the alumni IDs to join information and create a list of tuples with the .fetchall() method. This list of tuples was then passed to the "index.html" page using the render_template function, telling Flask to render "index.html", passing the list of tuples to the HTML page.
 #### HTML, Flask, & Jinja
In the "index.html" file, I set up a tile layer of Open Street Maps to display the United States. I linked the Leaflet maps stylesheet and JavaScript libraries to implement markers and popups on the map. I did this by using Jinja syntax to loop through the coordinate data passed from the tuple list of data from the SQLite3 table accessed in Python. My solution was to implement a separate layer for the markers and popups which both use Leaflet methods to access coordinates from the Jinja loop to be displayed on the map. Clicking on the map then links to another HTML page, "alumni.html," which displays alumni information.

The alumni.html page accesses, via the render_template function, a list of tuples from a SQLite3 "SELECT" operation in Python that includes alumni names, graduation years, cities, states, and employers. This is only for the students that have that information recorded in the Google Sheet. In the alumni.html file, the list is looped over, and the information is displayed in an HTML table.

  #### Final Thoughts
This is a functional web app. However, it will best function as the foundation for a fully contained MPRA alumni database and landing site. Obviously, this is a work in progress. I am currently working to improve and add more funcationality to the app. Future iterations will give alumni the ability to login, create a profile, and update their own information. Additionally, there will be more flexible options for data displayed to the users. Lastly, I plan to add backend access functionality for faculty members to edit data and see all the data. Furthermore, reports can be run to show trends in alumni careers, cities of employment, and any other data that could be collected.

 #### Included Operational Files
 - Python file: app.py
 - CSS file: styles.css
 - HTML files: layout.html, index.html, alumni.html
 - SQL files: alumni.db, databses.sql
 - md files: README.md
>>>>>>> mpra-alumni-app
