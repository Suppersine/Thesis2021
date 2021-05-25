# iaic lab network programming 2021/04/29 iAIC Lab 2021
from sys import argv
import os
import math
import requests
import random
import os.path
from os import path

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_url(zoom, xtile, ytile):
    subdomain = random.randint(1, 4)
    # https://a.tile.openstreetmap.org/{z}/{x}/{y}.png
    url = "https://c.tile.openstreetmap.org/%d/%d/%d.png" % (zoom, xtile, ytile)
    dir_path = "tiles/%d/%d/" % (zoom, xtile)
    download_path = "tiles/%d/%d/%d.png" % (zoom, xtile, ytile)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if(not os.path.isfile(download_path)):
        r = requests.get(url, stream=True)
        with open(download_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        fd.close()

def main(lat, lon,half_y,half_x):
    maxzoom = 3 #zz 
    # define ZZ by replacing it with an integer
    # from 0 to 6 download all
    for zoom in range(0,7,1):
        for x in range(0,2**zoom,1):
            for y in range(0,2**zoom,1):
                download_url(zoom, x, y)
    # from 6 to 15 ranges
    for zoom in range(7, int(maxzoom)+1, 1):
        xtile, ytile = deg2num(float(lat)-half_y, float(lon)-half_x, zoom)
        final_xtile, final_ytile = deg2num(float(lat)+half_y, float(lon)+half_x, zoom)
        for x in range(xtile, final_xtile + 1, 1):
            # print("%d:%d-%d/%d-%d" % (zoom, xtile, final_xtile, ytile, final_ytile))
            for y in range(ytile, final_ytile - 1, -1):                
                result = download_url(zoom, x, y)
    
    
    for zoom in range(13, 16, 1):
        xtile, ytile = deg2num(float(lat)-half_y, float(lon)-half_x, zoom)
        final_xtile, final_ytile = deg2num(float(lat)+half_y, float(lon)+half_x, zoom)
        for x in range(xtile, final_xtile + 1, 1):
            # print("%d:%d-%d/%d-%d" % (zoom, xtile, final_xtile, ytile, final_ytile))
            for y in range(ytile, final_ytile - 1, -1):                
                result = download_url(zoom, x, y)

# usage prog <lat> <lon>
if __name__ == '__main__':
    ntp_midx = 121.6381184 # longititude of center of new taipei city
    ntp_midy = 24.9731632  # latitude of center of new taipei city
    half_x = 0.368
    half_y = 0.325
    main(ntp_midy, ntp_midx,half_y,half_x)

'''
    ntp_midx = 121.6381184 # longititude of center of new taipei city
    ntp_midy = 24.9731632  # latitude of center of new taipei city
    half_x = 0.368
    half_y = 0.325
'''