#!/usr/bin/env python3

import argparse
import os
import random
import shapefile  # pip install pyshp
import sys
import requests
import multiprocessing
import getcolor
import pandas as pd
import creds

IMGS_PER_SOURCE = 100
LL_RANGE = 0.1
API_KEY = creds.API_KEY
GOOGLE_URL = ("http://maps.googleapis.com/maps/api/streetview?sensor=false&"
              "size=640x640&fov=120&key=" + API_KEY)
SELECTED_COUNTRIES = ['AUS', 'MEX', 'JPN', 'ITA', 'ZAF', 'ESP', 'FRA', 'TUR',
        'SWE', 'ARG', 'THA']

SELECTED_CITIES = ['Singapore', 'Sydney', 'Melbourne', 'Tokyo', 'Osaka',
        'Paris', 'Madrid', 'Barcelona', 'Rome', 'Venice',
        'San Francisco', 'New York', 'Stockholm', 'Johannesburg', 'Honolulu',
        'Cape Town', 'Sao Paulo', 'Buenos Aires', 'Bangkok', 'Ankara',
        'Seoul', 'Busan', 'Phnom Penh', 'Palermo', 'Athens', 'Vienna',
        'Prague', 'Warsaw', 'Taipei']

print("Threads: %d"%(multiprocessing.cpu_count()))
pool = multiprocessing.Pool(multiprocessing.cpu_count())

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
# http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def get_country_imgs(num, country, name, bbox, borders):
    attempts = 0
    outfile_base = "../imgs/Countries/"+country+"/"
    if not os.path.exists(outfile_base):
        os.makedirs(outfile_base)

    min_lon = bbox[0]
    min_lat = bbox[1]
    max_lon = bbox[2]
    max_lat = bbox[3]

    pending = []
    for i in range(num):
        while(True):
            rand_lat = random.uniform(min_lat, max_lat)
            rand_lon = random.uniform(min_lon, max_lon)

            if point_inside_polygon(rand_lon, rand_lat, borders):
                if get_img(outfile_base+"%s_%f_%f.jpg"%(name,rand_lat,rand_lon),
                        rand_lat,rand_lon):
                    break
                else:
                    attempts+=1
    return attempts

def get_city_imgs(num, country, name, lat, lon):
    attempts = 0
    outfile_base = "../imgs/Cities/"+country+"/"
    if not os.path.exists(outfile_base):
        os.makedirs(outfile_base)

    pending = []
    for i in range(num):
        rand_lat = lat+random.uniform(-LL_RANGE, LL_RANGE)
        rand_lon = lon+random.uniform(-LL_RANGE, LL_RANGE)

        while not get_img(outfile_base+"%s_%f_%f.jpg"%(name,rand_lat,rand_lon),
                rand_lat,rand_lon):
            rand_lat = lat+random.uniform(-LL_RANGE, LL_RANGE)
            rand_lon = lon+random.uniform(-LL_RANGE, LL_RANGE)

def get_img(outfile,lat,lon):
    attempts = 1
    lat_lon = str(lat) + "," + str(lon)
    url = GOOGLE_URL + "&location=" + lat_lon
    r = requests.get(url)
    with open(outfile,'wb') as f:
        f.write(r.content)
    with open(outfile,'rb') as f:
        color = getcolor.get_color(f)
        if color[0] == '#e3e2dd' or color[0] == "#e3e2de":
            attempts+=1
            os.remove(outfile)
            #print("No Image")
            return False
        else:
            print("Img %s downloaded."%(outfile))
            return True

print("Loading borders")
country_shape_file = "../Countries/TM_WORLD_BORDERS_SIMPL-0.3.shp"
city_shape_file = "../Cities/cities.shp"

if not os.path.exists(shape_file):
    print("Cannot find " + shape_file)
    sys.exit()

sf = shapefile.Reader(country_shape_file)

record_df = pd.DataFrame(sf.records(), columns=[e[0] for e in sf.fields[1:]])

def get_all_cities(record_df, sf):
    record_df = record_df.loc[record_df['NAME'].isin(SELECTED_CITIES)]
    selected_shapes = [sf.shapes()[i] for i in record_df.index]
    print(record_df)

    results = list()

    for i, shape in enumerate(selected_shapes):
        print("Loading:")
        record = record_df.iloc[i]
        print(record)

        lat, lon = shape.points[0]
        results.append(pool.apply_async(get_city_imgs(IMGS_PER_SOURCE, record["COUNTRY"],
            record["NAME"], lon, lat)))
    [r.get() for r in results]

def get_all_countries(record_df, sf):
    pass



