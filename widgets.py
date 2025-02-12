#----------------------imports------------------------------
import turtle
import geocoder
import pyowm
from time import sleep
import datetime

#--------------------file imports----------------------------
from helpers import getConfig, getKey, createTurtle

#----------------------------code-------------------------------\
#default widgetConfig
defaultWidgetConfig = {
            "xpos":0,
            "ypos":0,
            "color":"white",
            "widgetLength":250,
            "font":"Arial",
            "fontSize":34,
            "fontModifier":"normal",
            "xpos":0,
            "ypos":0,
            "updateFrequency":60
        }

#--------------------------widgets--------------------------------
class time:
    def __init__(self):
        #reading the config
        self.widgetConfig = getConfig(type(self).__name__, defaultWidgetConfig)

        #setting the position vars
        self.xpos = self.widgetConfig["xpos"] - (self.widgetConfig["widgetLength"] / 2)
        self.ypos = self.widgetConfig["ypos"]
        self.widgetFont = (self.widgetConfig["font"], self.widgetConfig["fontSize"], self.widgetConfig["fontModifier"])

        #creating the static content for the time defaulte widget
        turtle.tracer(1)
        self.mirrorTurtle = createTurtle(self.widgetConfig["color"],self.xpos, self.ypos)
        self.mirrorTurtle.pd()
        self.mirrorTurtle.forward(self.widgetConfig["widgetLength"])
        turtle.tracer(0)
        

        #creatinging the widgetTurtleTrue
        self.widgetTurtle = createTurtle(self.widgetConfig["color"],self.xpos + (self.widgetConfig["widgetLength"] / 2), self.ypos + 6)
        self.widgetTurtle.setheading(90)

        #self.update()


    def update(self):
        #getting the time and date
        now = datetime.datetime.now()
        
        currentTime = now.strftime("%I:%M %p")
        currentDate = now.strftime("%m-%d-%Y")

        #sending the time and date to the screen
        self.widgetTurtle.clear()
        self.widgetTurtle.write(currentTime, align="center", font=self.widgetFont)
        self.widgetTurtle.backward(56)
        self.widgetTurtle.write(currentDate, align="center", font=self.widgetFont)
        self.widgetTurtle.forward(56)

class weather:
    def __init__(self):
        #config for this specific widget
        widgetConfig = {
            "units":"Farenhight"
        }
        #reading the config
        self.widgetConfig = getConfig(type(self).__name__, {**widgetConfig, **defaultWidgetConfig})   

        #setting the position vars
        self.xpos = self.widgetConfig["xpos"] - (self.widgetConfig["widgetLength"] / 2)
        self.ypos = self.widgetConfig["ypos"]
        self.widgetFont = (self.widgetConfig["font"], self.widgetConfig["fontSize"], self.widgetConfig["fontModifier"])

        #creating the static content for the time defaulte widget
        turtle.tracer(1)
        self.mirrorTurtle = createTurtle(self.widgetConfig["color"],self.xpos, self.ypos)
        self.mirrorTurtle.pd()
        self.mirrorTurtle.forward(self.widgetConfig["widgetLength"])
        turtle.tracer(0)
    

        #creatinging the widgetTurtle
        self.widgetTurtle = createTurtle(self.widgetConfig["color"],self.xpos + (self.widgetConfig["widgetLength"] / 2), self.ypos)
        self.widgetTurtle.setheading(90)

        #setting up the API
        self.key = getKey(type(self).__name__)
        self.haskey = True
        if (self.key == ""):
            self.haskey = False
            print("[keys/" + type(self).__name__ + ".key] is blank please enter your api key into the file")
            self.widgetTurtle.write("API key not found", align="center", font=self.widgetFont)
            return

        self.lat, self.lon = geocoder.ip('me').latlng

        self.weather_getter = pyowm.OWM(self.key).weather_manager()
        

        #updateing to add the data
        #self.update()

    def update(self):
        #checking to see if there is a valid API key
        if (not(self.haskey)):
            return

        #calling the weather API
        try:
            current_weather = self.weather_getter.weather_at_coords(self.lat, self.lon)
        except pyowm.commons.exceptions.UnauthorizedError:
            #outputing an invalid weather API to the screen
            self.widgetTurtle.clear()
            self.widgetTurtle.write("Invalid weather API key", align="center", font=self.widgetFont)
            self.haskey = False
            return

        #organizeing the weather data
        weather = {
            "temperature":str(round(current_weather.weather.temperature("fahrenheit")["temp"])) + "\xb0 " + self.widgetConfig["units"][:1],
            "description":current_weather.weather.detailed_status,
            "sunset":current_weather.weather.sunset_time("date").strftime("%I:%M %p"),
        }
        
        self.widgetTurtle.clear()
        self.widgetTurtle.write(weather["temperature"], font=self.widgetFont)
        self.widgetTurtle.backward(56)
        self.widgetTurtle.write(weather["sunset"], align = "center", font=self.widgetFont)
        self.widgetTurtle.forward(56)
