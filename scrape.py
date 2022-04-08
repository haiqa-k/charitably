
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from json import JSONEncoder
import webbrowser
import time
import mysql.connector
import toolz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from serpapi import GoogleSearch #pip install google-search-results
from geopy.geocoders import Nominatim #pip install geopy


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

# headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
# url = 'https://www.meetup.com/find/events/?allMeetups=true&radius=25&userFreeform=New York, NY&mcId=c10001&mcName=New York, NY'

# response=requests.get(url,headers=headers)
# print(response)

# soup=BeautifulSoup(response.text,'html.parser')
# tag = soup.find_all('li')
# print(tag)
# for item in soup.select('.event-listing'):
#     print(item)
#     try:
#         print('----------------------------------------')
#         #print(item)
#         print(item.select('[itemProp=name]')[0].get_text())
#         print(item.select('[itemProp=name]')[1].get_text())

#         print(item.select('.omnCamp')[0].get_text().strip().replace('\n', ' '))
#         print(item.select('.attendee-count')[0].get_text().strip().replace('\n', ' '))

#     except Exception as e:
#         #raise e
#         print('')
def convert_date_eventbrite(date):
    year = date[:4]
    month = date[5:]
    date = month + '-' + year
    return date

def convert_date_google(date):
    date = date.strip()
    if(date[:3] == 'Jan'):
        if(len(date[4:]) == 1):
            new_date = '01-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '01-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Feb'):
        if(len(date[4:]) == 1):
            new_date = '02-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '02-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Mar'):
        if(len(date[4:]) == 1):
            new_date = '03-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '03-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Apr'):
        if(len(date[4:]) == 1):
            new_date = '04-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '04-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'May'):
        if(len(date[4:]) == 1):
            new_date = '05-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '05-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Jun'):
        if(len(date[4:]) == 1):
            new_date = '06-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '06-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Jul'):
        if(len(date[4:]) == 1):
            new_date = '07-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '07-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Aug'):
        if(len(date[4:]) == 1):
            new_date = '08-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '08-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Sep'):
        if(len(date[4:]) == 1):
            new_date = '09-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '09-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Oct'):
        if(len(date[4:]) == 1):
            new_date = '10-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '10-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Nov'):
        if(len(date[4:]) == 1):
            new_date = '11-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '11-'+date[4:]+'-2022'
            return new_date
    if(date[:3] == 'Dec'):
        if(len(date[4:]) == 1):
            new_date = '12-0'+date[4:]+'-2022'
            return new_date
        else:
            new_date = '12-'+date[4:]+'-2022'
            return new_date
    else: 
        return date

# Function: This function uses BeautifulSoup to scrape the Eventbrite website for charity events
# Input: int 'max' representing the number of events to retrieve
# Output: Returns a list of event objects 

def eventbrite_events(max):
    event_list = []

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    start = time.time()
    for i in range (max):
      
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
        s_date = item['startDate']
        start_date = convert_date_eventbrite(s_date)
        print(start_date)
        e_date = item['endDate']
        end_date = convert_date_eventbrite(e_date)
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

    end = time.time()
    print("Execution time: ", end-start)
    return event_list


# geo = [] #list to hold the geographical coordinates of each 
# for x in event_list:
#     coordinates = [float(x.latitude), float(x.longitude)]
#     geo.append(coordinates)
# print(geo)



# Function: This function uses BeautifulSoup to scrape the Eventbrite website for charity events
# Input: None
# Output: None
def google_events_bs4():

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }


    response = requests.get("https://serpapi.com/searches/e3d8c5d12dc868b5/623ff90dd5a531c3a4f267b7.html", headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    events_data = []
    num = 0
    for event in soup.select('.PaEvOc'):
        name = event.select_one('.YOGjf').text
        #link = event.select_one('.odIJnf a')['href']
        day = event.select_one('.gsrt.v14Sh.OaCVOb .UIaQzd').text
        month = event.select_one('.gsrt.v14Sh.OaCVOb .wsnHcb').text
        when = event.select_one('.cEZxRc:nth-child(1)').text
        address_street = event.select_one('.cEZxRc:nth-child(2)').text
        address_city = event.select_one('.cEZxRc:nth-child(3)').text
        date = day+" "+month
        print("Name: ", name)
        print("Date: ", date)
        print("When: ", when)
        print("Street: ", address_street)
        print("City: ", address_city)
        num = num+1
    print(num)

# Function: Uses the SERP API to scrape events from google events
#Input: int 'max' representing the number of events to retrieve
#Output: Returns a list of event objects scraped from google events using SERP API

def google_events_SERP(max):
    event_list = []
    start = 0 #this is an offset variable used to iterate through the events for some reason, one search is retreiving only 10 results therefore, to retreive more events, 
              #I am doing multiple searches and each search is offset by 10 so that the previously retreived events are not retreived again
    count = 0 #variable used to keep a count of the number of events retreived
    try:
        while (start < max): #the number acts as a cap for the total events retreived


            params = {
                "api_key": "85c26552886cb11adff784f9668a7b3b553122ff2d56286555dedb2f3dea0e0e",
                "engine": "google_events",
                "q": "Charity", #query = charity events
                "gl": "us", #location = U.S.
                "hl": "en", #language = english
                "start": start,
                "device": "desktop"
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            #print(results)
            geolocator = Nominatim(user_agent="geoapiExercises")

            for item in results['events_results']:
                #print(json.dumps(item, indent=2, ensure_ascii=False))
                name = item['title']
                try:
                    date = item['date']
                    s_date = date.get('start_date')
                    start_date = convert_date_google(s_date)
                    print('start date: ', s_date, 'new: ', start_date)
                except:
                    date = ""
                try:
                    address = item['address']
                    street = address[0]
                    city = address[1]
                except:
                    address = ""
                    street = ""
                    city = ""
                try:
                    url = item['link']
                except:
                    url = ""
                try:
                    description = item['description']
                except:
                    description = ""
                
                location = geolocator.geocode(city) #using python geopy
                try:
                    data = location.raw
                    latitude = data['lat']
                    longitude = data['lon']
                    location = geolocator.reverse((latitude, longitude)) #using geopy to retrive zipcode using coordinates
                    try:
                        postal_code = location.raw['address']['postcode']
                    
                    except:
                        postal_code = "" #for certain locations, the return is None so to handle that
                except:
                    latitude = ""
                    longitude = ""
                    postal_code = ""
                end_date = start_date
                try:
                    country = location.address.split(",")[-1]
                except:
                    country = ""
                try:
                    state = location.address.split(",")[-3]
                except:
                    state = ""
                count = count + 1
                # print(count, "). ", name)
                # print(description)
                # print(street)
                # print(city)
                # print(postal_code)
                # print()
                event_list.append(events(name, url, start_date, end_date, address, country, state, street, postal_code, longitude, latitude, description))
            #print(count)
            start = start+10 #offsetting by 10 so that the next search takes skips the 10 events previously retreived
    except:
        print("Total Events Recorded: ",count)
    return event_list



# #Calling the functions to retrive events and collecting them in one list
event_list = eventbrite_events(1)
event_list1 = google_events_SERP(1)
event_list.extend(event_list1)
print("Event list length: ",len(event_list))
for i in range(len(event_list)):
    print(i, event_list[i].name, event_list[i].postal_code, event_list[i].start_date)


#toolz.unique returns a generator object without any duplicates from event_list
unique = list(toolz.unique(event_list, key=lambda x: x.name))

#making sure that all the events in the list are unique (avoiding repeated events)
z=[]
for i in unique:
    z.append(i.postal_code)
l = []
for k in z:
    l.append([k, z.count(k)])

# #store the data to the table Events in the database Charitably
# for x in event_list:
#     check_name = [x.name]
#     #check if the event is already present in the table
#     mycursor.execute("SELECT name, COUNT(*) FROM Events WHERE name = %s GROUP BY name", check_name)
#     mycursor.fetchall()
#     row_count = mycursor.rowcount
#     if row_count == 0: #if event is not present in the table then row_count should be 0
#         sql_command = """INSERT INTO Events(name, url, start_date, end_date, address, street, country, state, postal_code, longitude, latitude, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#         name = str(x.name)
#         url = str(x.url)
#         start_date = str(x.start_date)
#         end_date = str(x.end_date)
#         address = str(x.address)
#         street = str(x.street)
#         country = str(x.country)
#         state = str(x.state)
#         postal_code = str(x.postal_code)
#         longitude = str(x.longitude)
#         latitude = str(x.latitude)
#         description = str(x.description)
#         values = [(name, url, start_date, end_date, address, street, country, state, postal_code, longitude, latitude, description)]
#         mycursor.executemany(sql_command, values)
#         db.commit()


#To list all the events in the database and their count
# mycursor.execute("SELECT * FROM Events")
# count = 0
# for x in mycursor:
#     count += 1
#     print(x)
# print("Total events in database: ", count)

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





