#To integrate html and python file
from flask import Flask, request, render_template
#creating the map
import folium 
#creating the browser that pops up
import webview 
#letting a program ran while excuting
import threading 
import googlemaps
from datetime import datetime  
import requests
from folium import Element

app = Flask(__name__)

user_lat = None
user_lon = None
dir_lat = None
dir_lon = None
time = 0 
search_data = ''
map = ''


g_place_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


#search function: Create a search bar using html and inject it into the map 
Search_html = f'''
<div id="search" style="position: absolute; top: 10px; left: 50px; background-color: white; padding: 10px; border-radius: 5px; z-index: 10000">
    <form action = '/search_data' method = 'POST'>
                <input type ='text' id='userInput' name='userInput' placeholder='Search'>
                <input type = 'Submit' value = 'Submit'>
    </form>
    <form action = '/direction_data' method = 'POST'>
        <input type = 'Submit' value = 'Direction'>
    </form>
</div>
'''
Search_html = Element(Search_html)


#Creates the map base on the area around parameters lat and lon
#Creates a marker at where the parameters lat and lon is
def create_map(t_lat, t_lon):
    global Search_html, map, user_lat, user_lon
    user_lat = t_lat 
    user_lon = t_lon
    #creates a variable map which takes from the folium library and creates a map
    map = folium.Map(location=[t_lat, t_lon], zoom_start = 15)
    #Creates a marker, parameters(location, what will pop up when hovered, icon).add_to(which foilum map variable are we adding this to?)
    folium.Marker(location = [t_lat, t_lon], popup = " You", icon = folium.Icon(color='red', icon='flag')).add_to(map)     
    #creates a new file and puts the code of the variable map into it
    
    map.get_root().html.add_child(Search_html)
    
    map.save("templates/map.html")

def create_marker(lat, lon, name):
    global Search_html, map
    #Creates a marker, parameters(location, what will pop up when hovered, icon).add_to(which foilum map variable are we adding this to?)
    folium.Marker(location = [lat, lon], popup = name, icon = folium.Icon(color='blue', icon='flag')).add_to(map)     
    
    map.get_root().html.add_child(Search_html)
    
    map.save("templates/map.html")
    
def create_direction(waypoints):
    global dir_lon, dir_lat, user_lat, user_lon, map
    
    folium.PolyLine(
        locations=waypoints,
        color="#FF0000",
        weight=2.5,
        tooltip='direction',
        smooth_factor='0'
    ).add_to(map)
    
    map.save('templates/map.html')

#creates the window (name, file to open)
def create_map_window():
    webview.create_window("INteractive Penn State Map", "templates/map.html")
    webview.start()

#Opens a website that gets your exact location then starts a webview, when it closes create_map_window() function is called 
def create_find_location():
    webview.create_window("Find your location", "http://127.0.0.1:5000/")
    webview.start() 
    
       
#Starts the background proccess for backend and frontend, the connect between the html file and python file 
def start_web():
    app.run(debug=True, use_reloader=False) 

#Opens and renders the template for get_location.html
@app.route('/')
def initial(): 
    return render_template('get_location.html')

#Using POST method, we are able to get the neccessary data for lat and lon that we got from the location in get_location.html
@app.route('/data', methods=['POST'])
def access_data():
    create_map(float(request.form.get('lat')), float(request.form.get('lon')))
    
    return render_template('home.html')

@app.route('/time_data', methods=['POST'])
def access_time_data():
    global time
    time = request.form.get('time')
    return render_template('map.html') 

@app.route('/search_data', methods=['POST'])
def Search():
    try :
        global search_data, user_lat, user_lon, dir_lat, dir_lon
        
        create_map(user_lat, user_lon)
        search_data = request.form.get('userInput')
    
        g_search = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': search_data,
            'key': api_key,
            'locationbias': f'point:{user_lat}, {user_lon}'
        }
    
        response = requests.get(g_search, params=params)
        data = response.json()
    
        if search_data:
            dir_lat = float(data['results'][0]['geometry']['location']['lat'])
            dir_lon = float(data['results'][0]['geometry']['location']['lng'])
            dir_name = data['results'][0]['name']
            create_marker(dir_lat, dir_lon, dir_name)
    except:
        pass
    return render_template('map.html')

@app.route('/direction_data', methods=['POST'])
def direction_data():
    global user_lat, user_lon, dir_lon, dir_lat
    
    g_direction = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'destination': f'{dir_lat}, {dir_lon}',
        'origin': f'{user_lat}, {user_lon}',
        'key': api_key, 
        'mode': 'walking'
    }
    
    response = requests.get(g_direction, params=params)
    data = response.json() 
    waypoints = [] 
    
    try:
        if 'routes' in data:
            routes = data['routes'][0]
            for route in routes['legs']:
                for step in route['steps']:
                    start_lat = step['start_location']['lat']
                    start_lon = step['start_location']['lng']
                    waypoints.append((start_lat, start_lon))
                    end_lat = step['end_location']['lat']
                    end_lon = step['end_location']['lng']
                    waypoints.append((end_lat, end_lon))
    except:
        pass
    create_direction(waypoints)
    print(waypoints)
    return render_template('map.html') 

if __name__ == '__main__':
    app_thread = threading.Thread(target=start_web)
    app_thread.start()
    create_find_location()

    




    
    

    


    
    
