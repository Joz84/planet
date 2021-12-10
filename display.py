import requests
from bs4 import BeautifulSoup
import random 
import plotly.express as px
import numpy as np

def lin_scale(radius, bounds):
    a = (bounds['screen_max'] - bounds['screen_min']) / (bounds['space_max'] - bounds['space_min'])
    b = bounds['screen_max'] - a * bounds['space_max']
    return a * radius + b

def hex_to_rgba_str(hex, a):
    rgb = [str(int(hex.lstrip('#')[i:i+2], 16)) for i in (0, 2, 4)]
    rgb.append(str(a))
    return f"rgba({', '.join(rgb)})"

def sun_color(temperature, bounds):
    normed_r = lin_scale(temperature, bounds)
    panel = px.colors.sequential.Plasma
    color_hex = panel[int(normed_r)]
    return hex_to_rgba_str(color_hex, 0.4)

def planet_color(temperature, bounds):
    normed_r = lin_scale(temperature, bounds)
    panel = px.colors.sequential.Turbo
    color_hex = panel[int(normed_r)]
    return hex_to_rgba_str(color_hex, 0.4)

def display(params):
    ##############################
    ### Echelles de conversion ###
    ##############################
    images = {
        "pluto":'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/pluto.jpg',
        "jupiter":'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/jupiter.jpg',
        "mercury":'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/mercury2.jpg',
        "neptune": 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/neptune.jpg'
    }

    planet_bounds = {
        'screen_min': 0,    'screen_max': 10,
        'space_min': 50,     'space_max': 4051,      
        }

    sun_bounds = {
        'screen_min': 0,    'screen_max': 10,
        'space_min': 575,     'space_max': 57001,        
        }

    size_bounds = {
        'screen_min': 200,    'screen_max': 400,
        'space_min': 200,     'space_max': 400,        
    }
    
    shadow_bounds = {
        'screen_min': -90,    'screen_max': -20,
        'space_min': -90,     'space_max': -20,        
    }
    
    s_intensity_bounds = {
        'screen_min': 20,    'screen_max': 90,
        'space_min': 20,     'space_max': 90,        
    }
    
    ###############################
    ### Récupération des params ###
    ###############################
    category = params["category"]
    radius = params["radius"]
    sun_temperature = params["sun_temperature"]
    sun_distance = params["sun_distance"]
    temperature = params["temperature"]
    luminosity = params["luminosity"]
    
    tilt = params.get("tilt", random.randrange(30))
    rotation_speed = params.get("rotation_speed", random.randrange(20,200))
    
    ################################
    ### Conversion des grandeurs ###
    ################################
    image = images[category]
    size = lin_scale(radius, size_bounds)
    p_color = planet_color(temperature, planet_bounds)
    shadow = lin_scale(luminosity, shadow_bounds)
    s_color = sun_color(sun_temperature, sun_bounds)
    s_intensity = lin_scale(sun_distance, s_intensity_bounds)
        
        
    #######################
    ### Stringification ###  
    #######################  
    root_infos = ['<style>:root {',
        f'--image: url("{image}");',
        f'--tilt: rotate({tilt}deg);',
        f'--rotation-speed: {rotation_speed};',
        f'--size: {size}px;',
        f'--color: {p_color};',
        f'--shadow: {shadow}px;',
        f'--sun-color: {s_color};',
        f'--sun-intensity: {s_intensity}px;'
        '}</style>',
    ]
    
    url = 'https://raw.githubusercontent.com/Joz84/planet/master/template.html'
    response = requests.get(url).content
    html_content = BeautifulSoup(response, "html.parser").prettify()
        
    return ' '.join(root_infos) + html_content


#### Exemples ####

params1 = {
'category': 'pluto',
'radius': 100,
'sun_temperature': 56000,
'sun_distance': 90,
'temperature': 4000,
'luminosity': -50,
}

params2 = {
'category': 'jupiter',
'radius': 300,
'sun_temperature': 600,
'sun_distance': 20,
'temperature': 50,
'luminosity': -90,
}

print(display(params1))
    