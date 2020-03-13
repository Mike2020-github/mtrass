# -*- coding: Windows-1251 -*-
import pandas as pd
import numpy as np
import folium
#from folium.plugins import MarkerCluster
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://trassagk.ru/trassa_azs/locator/')
soup = BeautifulSoup(html, 'html.parser')
dt = soup.find_all("td", class_="address")

map = folium.Map(location=[55.753215,37.622504], zoom_start = 9)

cena = pd.read_csv('http://trassagk.ru/trassa_azs/locator/?downloadlist=Y', ';', encoding='Windows-1251', nrows=53, usecols=[5], dtype={'5':np.float64})
cena_min = float(cena.min(skipna=True).iloc[0].replace(',','.'))
cena_max = float(cena.max(skipna=True).iloc[0].replace(',','.'))

def color_change(cc):
    plus = (cena_max - cena_min)/3
    if(cc == 0):
        return('blue')
    elif(cc < cena_min + plus):
        return('green')
    elif(cena_min + plus < cc < 44.49):
        return('orange')
    else:
        return('red')

i=0
for k in dt:
    for coord in k.find('a')['rel']:
        lst = coord.split(',')
        lat = lst[0]
        lon = lst[1]

        try:
            cc = float(cena.iloc[i, 0].replace(',','.'))
        except:
            cc = 0

        folium.Marker(location=[lat, lon], popup = str(cc), tooltip= str(cc), icon=folium.Icon(color = color_change(cc))).add_to(map)
        i += 1

map.save("map.html")