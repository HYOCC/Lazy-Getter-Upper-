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

user_lat, user_lon, dir_lat, dir_lon, dir_name= None, None, None, None, None
search_data = ''
map = ''
mode = 'walking'
html = None
direction_time_text = None
time_hours, time_minutes, direction_time = 0, 0, 0

api_key = 'AIzaSyBEfwcLaeTTEdXHw1eefzm6i-3oS51e1WY'

g_place_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


#search function: Create a search bar using html and inject it into the map 
def Search_html(time_display):
    return f'''
        <div id="search" style="position: absolute; top: 10px; left: 50px; background-color: rgba(255, 255, 255, 0.0); padding: 10px; width: 700px; border-radius: 5px; z-index: 10000">
            <div id = 'search_bar' style="display: flex";>
                <form action = '/search_data' method = 'POST'>
                    <input type ='text' id='userInput' name='userInput' placeholder='Search'>

                    <select id = 'target_hour' name = 'target_hour'>
                        <option value = '1'>1</option>
                        <option value = '2'>2</option>
                        <option value = '3'>3</option>
                        <option value = '4'>4</option>
                        <option value = '5'>5</option>
                        <option value = '6'>6</option>
                        <option value = '7'>7</option>
                        <option value = '8'>8</option>
                        <option value = '9'>9</option>
                        <option value = '10'>10</option>
                        <option value = '11'>11</option>
                        <option value = '12'>12</option>
                    </select>
                    <p style="display: inline;">:</p>
                    <select id = 'target_min' name = 'target_min'>
                        <option value = '0'>00</option>
                        <option value = '5'>05</option>
                        <option value = '10'>10</option>
                        <option value = '15'>15</option>
                        <option value = '20'>20</option>
                        <option value = '25'>25</option>
                        <option value = '30'>30</option>
                        <option value = '35'>35</option>
                        <option value = '40'>40</option>
                        <option value = '45'>45</option>
                        <option value = '50'>50</option>
                        <option value = '55'>55</option>
                    </select>

                    <select id = 'target_AM-or-PM' name = 'target_AM-or-PM'>
                        <option value='AM'>AM</option>
                        <option value="PM">PM</option>
                    </select>

                    <input type = 'Submit' value = 'Submit'>
                </form>
                    <form action ='/calculate', method = 'POST'>
                        <input type = 'Submit' value= 'Calculate'>
                    </form>
            </div>
            <form action = '/direction_data' method = 'POST'>
                <input type = 'Submit' value = 'Direction'>
            </form>

            <div id="modes" style="display: flex;">
                <form action='/bicycling_mode' method='POST'>
                    <input type='hidden' id='bicycling' name='bicycling' value='bicycling'>
                    <input type="Submit" value="Cycle">
                </form>
                
                <form action='/walking_mode' method='POST'>
                    <input type='hidden' id='walking' name='walking' value='walking'>
                    <input type="Submit" value="Walk">
                </form>
                
                <form action='/driving_mode' method='POST'>
                    <input type='hidden' id='driving' name='driving' value='driving'>
                    <input type="Submit" value="driving">
                </form>
                
                <form action='/transit_mode' method='POST'>
                    <input type='hidden' id='transit' name='transit' value='transit'>
                    <input type="Submit" value="transit">
                </form>

            </div>

            <div id ='time_label' style='color: red; display: flex; width: 100px;'>
                <p><b>Time:{time_display}</b></p>
            </div>
        </div>
    '''

#Creates the map base on the area around parameters lat and lon
#Creates a marker at where the parameters lat and lon is
def create_map(t_lat, t_lon):
    global map, user_lat, user_lon, html, direction_time_text
    user_lat = t_lat 
    user_lon = t_lon
    #creates a variable map which takes from the folium library and creates a map
    map = folium.Map(location=[t_lat, t_lon], zoom_start = 15)
    #Creates a marker, parameters(location, what will pop up when hovered, icon).add_to(which foilum map variable are we adding this to?)
    folium.Marker(location = [t_lat, t_lon], popup = " You", icon = folium.Icon(color='red', icon='flag')).add_to(map)     
    #creates a new file and puts the code of the variable map into it
    
    html = Element(Search_html(direction_time_text))
    map.get_root().html.add_child(html)
    map.save("templates/map.html")

def create_marker(lat, lon, name):
    global html, map
    #Creates a marker, parameters(location, what will pop up when hovered, icon).add_to(which foilum map variable are we adding this to?)
    folium.Marker(location = [lat, lon], popup = name, icon = folium.Icon(color='blue', icon='flag')).add_to(map)     
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
    webview.create_window("InNteractive Penn State Map", "templates/map.html")
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
    global user_time
    user_time = request.form.get('time')
    if user_time:
        user_time = int(user_time)
    else:
        user_time = 0
    return render_template('map.html') 

@app.route('/search_data', methods=['POST'])
def Search():
    global search_data, user_lat, user_lon, dir_lat, dir_lon, dir_name, time_hours, time_minutes, direction_time_text, direction_time
    try:
        
        search_data = request.form.get('userInput')
        g_direction = 'https://maps.googleapis.com/maps/api/directions/json'
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
            
            direction_params = {
                'destination': f'{dir_lat}, {dir_lon}',
                'origin': f'{user_lat}, {user_lon}',
                'key': api_key, 
                'mode': mode
            }
            data_direction = requests.get(g_direction, params=direction_params).json() 
            direction_time_text = data_direction['routes'][0]['legs'][0]['duration']['text']
            direction_time = int(data_direction['routes'][0]['legs'][0]['duration']['value'])
            create_map(user_lat, user_lon)
            create_marker(dir_lat, dir_lon, dir_name)
    except:
        pass
        
    if request.form.get('target_AM-or-PM') == 'PM':
        time_hours = int(request.form.get('target_hour')) + 12
    else:
        time_hours = int(request.form.get('target_hour'))
        time_minutes = int(request.form.get('target_min'))
        
    return render_template('map.html')

@app.route('/direction_data', methods=['POST'])
def direction_data():
    global user_lat, user_lon, dir_lon, dir_lat, dir_name, html, mode
    
    g_direction = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'destination': f'{dir_lat}, {dir_lon}',
        'origin': f'{user_lat}, {user_lon}',
        'key': api_key, 
        'mode': mode
    }
    
    data = requests.get(g_direction, params=params).json() 
    waypoints = [] 
    warnings = []

    try:
        if 'routes' in data:
            routes = data['routes'][0]
            
            if 'warnings' in data['routes'][0] and data['routes'][0]['warnings']:
                for warning in data['routes'][0]['warnings']:
                    warnings.append(warning)
                    ' '.join(warnings)
                
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
    
    else: create_map(user_lat, user_lon)
    create_marker(dir_lat, dir_lon, dir_name)
    create_direction(waypoints)
    return render_template('map.html')

@app.route('/bicycling_mode', methods=["POST"])
def cycle_mode():
    global mode
    mode = request.form.get('bicycling')
    if dir_lat and dir_lon:
        return direction_data()
    return render_template('map.html')

@app.route('/transit_mode', methods=["POST"])
def transit_mode():
    global mode
    mode = request.form.get('transit')
    if dir_lat and dir_lon:
        return direction_data()
    return render_template('map.html')

@app.route('/walking_mode', methods=["POST"])
def walking_mode():
    global mode
    mode = request.form.get('walking')
    if dir_lat and dir_lon:
        return direction_data()
    return render_template('map.html')

@app.route('/driving_mode', methods=["POST"])
def driving_mode():
    global mode
    mode = request.form.get('driving')
    if dir_lat and dir_lon:
        return direction_data()
    return render_template('map.html')

@app.route('/calculate', methods=["POST"])
def calculate():
    global user_time, time_hours, time_minutes, direction_time
    
    error_minutes = 8
    calc_minutes = time_minutes - (user_time + (direction_time // 60))
    
    if calc_minutes < 0:
        time_hours -= max((abs(calc_minutes) // 60), 1)
        calc_minutes = -(abs(calc_minutes) % 60) + 60
        
    if time_hours < 1:
        if time_hours == 0:
            time_hours = 24
        else: 
            time_hours %= 24
    
    if time_hours > 12:
        AM_PM = 'PM'
        time_hours -= 12 
    else:
        AM_PM = 'AM'
    
    if time_minutes < 10:
        time_minutes = '0' + str(time_minutes)
    
    calc_minutes += error_minutes
    
    return render_template('result.html', hours = time_hours, minutes = calc_minutes, status = AM_PM)    

if __name__ == '__main__':
    app_thread = threading.Thread(target=start_web)
    app_thread.start()
    create_find_location()
    

    




    
    

    


    
    
