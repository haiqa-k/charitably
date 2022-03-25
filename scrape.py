
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from json import JSONEncoder
import webbrowser
import time
import mysql.connector
import toolz


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "myproject",
    database = "charitably"
    )

mycursor = db.cursor()

#mycursor.execute("CREATE DATABASE charitably") #The database "charitably" is created

# mycursor.execute("DROP TABLE Events") #to delete table
# mycursor.execute("CREATE TABLE Events(name VARCHAR(150), url VARCHAR(500), start_date VARCHAR(20),end_date VARCHAR(20),address VARCHAR(500), street VARCHAR(200), country VARCHAR(50), state VARCHAR(20), postal_code VARCHAR(20), longitude VARCHAR(100), latitude VARCHAR(100),description VARCHAR(500), eventID int PRIMARY KEY AUTO_INCREMENT)") #creating a table inside my database
# mycursor.execute("CREATE TABLE AllEvents(name VARCHAR(150), url VARCHAR(500), start_date VARCHAR(20),end_date VARCHAR(20),address VARCHAR(500), street VARCHAR(200), country VARCHAR(50), state VARCHAR(20), postal_code VARCHAR(20), longitude VARCHAR(100), latitude VARCHAR(100),description VARCHAR(500), eventID int PRIMARY KEY AUTO_INCREMENT)") #creating a table inside my database


class events: 
    def __init__(self, name, url, start_date, end_date, address, country, state, street, postal_code, longitude, latitude, description): 
        self.name = name 
        self.url = url
        self.start_date = start_date
        self.end_date = end_date
        self.address = address
        self.country = country
        self.state = state
        self.street = street
        self.postal_code = postal_code
        self.longitude = longitude
        self.latitude = latitude
        self.description = description
def encoder_events(event):
    # if isinstance(event, events):
    return{'name': event.name, 'url': event.url, 'start_date': event.start_date, 'end_date': event.end_date, 'address': event.address, 'country': event.country, 'state': event.state, 'street': event.street, 'postal_code':event.postal_code, 'longitude':event.longitude, 'latitude': event.latitude, 'description': event.description}
    # raise TypeError(f'Object {event} is not of type events')

event_list = []

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
for i in range (40):
  
  page = str(i)
  url_base = 'https://www.eventbrite.com/d/united-states/charity-and-causes--events/?page='
  url_ = url_base + page

  result=requests.get(url_,headers=headers)
  doc=BeautifulSoup(result.text,"html.parser")
  #print(doc)
  tag = doc.find_all("script") #returns all the <script> tags
  #print(tag)
  tag_length = len(tag)
  script = tag[tag_length-1] #get the last <script> tag
  #print(script)
  json_list = json.loads(script.contents[0]) #returns a list of json 
  #print(json_list)

  for item in json_list:
    name = item['name']
    url = "https://www.google.com/search?q="+name.replace(" ", "+");
    print("Name of the event: ",name)
    start_date = item['startDate']
    print("Start data: ",item['startDate'])
    end_date = item['endDate']
    print("End date: ",end_date)
    location = item['location']
    address = location.get('address')
    country = address.get('addressCountry')
    state = address.get('addressRegion')
    street = address.get('streetAddress')
    postal_code = address.get('postalCode')
    print("ZIP code of the event: ",postal_code)
    geo =  location.get('geo')
    latitude = geo.get('latitude')
    longitude = geo.get('longitude')
    print("Address: ", street, ", ", state, ", ",country, ", ",postal_code)
    description = item['description']
    print("Description: ",description)
    event_list.append(events(name, url, start_date, end_date, address, country, state, street, postal_code, longitude, latitude, description))
    print("**********************************\n")

#store the data to the table Events in the database Charitably
for x in event_list:
    check_name = [x.name]
    #check if the event is already present in the table
    mycursor.execute("SELECT name, COUNT(*) FROM Events WHERE name = %s GROUP BY name", check_name)
    mycursor.fetchall()
    row_count = mycursor.rowcount
    if row_count == 0: #if event is not present in the table then row_count should be 0
        sql_command = """INSERT INTO Events(name, url, start_date, end_date, address, street, country, state, postal_code, longitude, latitude, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        name = str(x.name)
        url = str(x.url)
        start_date = str(x.start_date)
        end_date = str(x.end_date)
        address = str(x.address)
        street = str(x.street)
        country = str(x.country)
        state = str(x.state)
        postal_code = str(x.postal_code)
        longitude = str(x.longitude)
        latitude = str(x.latitude)
        description = str(x.description)
        values = [(name, url, start_date, end_date, address, street, country, state, postal_code, longitude, latitude, description)]
        mycursor.executemany(sql_command, values)
        db.commit()


#To list all the events in the database and their count
# mycursor.execute("SELECT * FROM Events")
# count = 0
# for x in mycursor:
#     count += 1
#     print(x)
# print("Total events in database: ", count)



# geo = [] #list to hold the geographical coordinates of each 
# for x in event_list:
#     coordinates = [float(x.latitude), float(x.longitude)]
#     geo.append(coordinates)
# print(geo)




#toolz.unique returns a generator object without any duplicates from event_list
unique = list(toolz.unique(event_list, key=lambda x: x.name))

z=[]
for i in unique:
    z.append(i.postal_code)
l = []
for k in z:
    l.append([k, z.count(k)])
print(l)
    
app = Flask(__name__, static_url_path='')

@app.route('/home/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        zipcode = request.form["zipcode"]
        return redirect(url_for("events", zip = zipcode)) #pass the zipcode to the list view page 
    else:
        return render_template('search.html')

@app.route('/map/<zip>')
def map_func(zip):
    mylist = []
    for i in unique:
        if i.postal_code == zip: #compare the inputted zipcode with all the zipcodes in the event list 
            k = json.dumps(i, default = encoder_events)
            mylist.append(k)
    return render_template('demo.html', list=mylist, zip = zip)


@app.route("/list/<zip>")
def events(zip):
    zips = []
    for i in unique:
        if i.postal_code == zip: #compare the inputted zipcode with all the zipcodes in the event list 
            zips.append(i)
    print(zip)
    return render_template('scrape.html', list = zips, zip = zip) #only send a list of events of the inputted zipcode

if __name__ == '__main__':
    app.run(debug = True)







