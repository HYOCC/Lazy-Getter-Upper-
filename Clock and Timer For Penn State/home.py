#To integrate html and python file
from flask import Flask, request, render_template
#creating the map
import folium
#creating the browser that pops up
import webview 
#letting a program ran while excuting
import threading 

app = Flask(__name__)

lat = None
lon = None


#Creates the map base on the area around parameters lat and lon
#Creates a marker at where the parameters lat and lon is
def create_map(lat, lon):
    #creates a variable map which takes from the folium library and creates a map
    map = folium.Map(location=[lat, lon], zoom_start = 15)
    #Creates a marker, parameters(location, what will pop up when hovered, icon).add_to(which foilum map variable are we adding this to?)
    folium.Marker(location = [lat, lon], popup = " You", icon = folium.Icon(color='red', icon='flag')).add_to(map)
    #creates a new file and puts the code of the variable map into it
    map.save("templates/map.html")


#creates the window (name, file to open)
def create_map_window():
    webview.create_window("INteractive Penn State Map", "templates/map.html")
    webview.start()

#Opens a website that gets your exact location then starts a webview, when it closes create_map_window() function is called 
def create_find_location():
    webview.create_window("Find your location", "http://127.0.0.1:5000/")
    webview.start() 
    create_map_window()

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
    global lat, lon
    lat = "found"
    lon = "found"
    create_map(request.form.get('lat'), request.form.get('lon'))
    return 'location found'

if __name__ == '__main__':
    app_thread = threading.Thread(target=start_web)
    app_thread.start()
    create_find_location()
    




    
    

    


    
    
