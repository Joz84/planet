import requests
from bs4 import BeautifulSoup
import random 
import plotly.express as px
import numpy as np


# def log_scale(radius, bounds):
#     return 1


def lin_scale(radius, bounds):
    a = (bounds['screen_max'] - bounds['screen_min']) / (bounds['space_max'] - bounds['space_min'])
    b = bounds['screen_max'] - a * bounds['space_max']
    return a * radius + b

def log_scale(radius, bounds):
    a = (np.exp(bounds['screen_max']) - np.exp(bounds['screen_min'])) / (bounds['space_max'] - bounds['space_min'])
    b = np.exp(bounds['screen_max']) - a * bounds['space_max']
    return b


# bounds = {
#     'screen_min': 1,
#     'screen_max': 10,
#     'space_min': 10,
#     'space_max': 1000,        
#     }
# normed_r = log_scale(5, bounds)
# print(normed_r)

def hex_to_rgba_str(hex, a):
    rgb = [str(int(hex.lstrip('#')[i:i+2], 16)) for i in (0, 2, 4)]
    rgb.append(str(a))
    return f"rgba({', '.join(rgb)})"

def sun_color(temperature):
    bounds = {
        'screen_min': 0,    'screen_max': 10,
        'space_min': 575,     'space_max': 57000,        
        }
    normed_r = lin_scale(temperature, bounds)
    panel = px.colors.sequential.Plasma
    color_hex = panel[int(normed_r)]
    return hex_to_rgba_str(color_hex, 0.4)

def planet_color(temperature):
    bounds = {
        'screen_min': 0,    'screen_max': 10,
        'space_min': 50,     'space_max': 4050,      
        }
    normed_r = lin_scale(temperature, bounds)
    panel = px.colors.sequential.Turbo
    color_hex = panel[int(normed_r)]
    return hex_to_rgba_str(color_hex, 0.4)

def coco(params):
    category = params["category"]
    radius = params["radius"]
    sun_temperature = params["sun_temperature"]
    sun_distance = params["sun_distance"]
    temperature = params["temperature"]
    luminosity = params["luminosity"]
    
    tilt = params.get("tilt", random.randrange(30))
    rotation_speed = params.get("rotation_speed", random.randrange(20,200))

    images = {
        "riri":'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/pluto.jpg',
        "fifi":'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/pluto.jpg',
        "loulou":'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/pluto.jpg',
    }
    image = images[category]

    # 200 : 400
    size_bounds = {
        'screen_min': 200,    'screen_max': 400,
        'space_min': 200,     'space_max': 400,        
    }
    size = lin_scale(radius, size_bounds)
       
    p_color = planet_color(temperature)
    
    #-20 : -90
    shadow_bounds = {
        'screen_min': -90,    'screen_max': -20,
        'space_min': -90,     'space_max': -20,        
    }
    shadow = lin_scale(luminosity, shadow_bounds)
    
    s_color = sun_color(sun_temperature)
    
    # 20 : 90
    s_intensity_bounds = {
        'screen_min': 20,    'screen_max': 90,
        'space_min': 20,     'space_max': 90,        
    }
    s_intensity = lin_scale(sun_distance, s_intensity_bounds)
        
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

params1 = {
'category': 'riri',
'radius': 100,
'sun_temperature': 56000,
'sun_distance': 70,
'temperature': 500,
'luminosity': -70,
}

params2 = {
'category': 'riri',
'radius': 100,
'sun_temperature': 56000,
'sun_distance': 70,
'temperature': 500,
'luminosity': -70,
}

print(coco(params1))
    