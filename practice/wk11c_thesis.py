# 2021/05/03 iaic lab network programming iAIC Lab
import json 
import matplotlib.pyplot as plt 
import math
import os
import os.path
from os import path
import numpy as np
from PIL import Image
from PIL import ImageDraw

TINT_COLOR = (0, 0, 255)  # BLUE
TRANSPARENCY = .30  # Degree of transparency, 0-100%
OPACITY = int(255 * TRANSPARENCY)
BLUE  = '#6699cc'
BLACK = '#000000'

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xf_num = (lon_deg + 180.0) / 360.0 * n
  xtile = int(xf_num)
  yf_num = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
  ytile = int(yf_num)
  tile_posx = int(256.0*(xf_num-xtile))
  tile_posy = int(256.0*(yf_num-ytile))
  return (xtile,ytile,tile_posx,tile_posy)

def deg2posXY(xmin_idx,ymin_idx,lat_deg,lon_deg,zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xf_num = (lon_deg + 180.0) / 360.0 * n
  xtile = int(xf_num)
  yf_num = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
  ytile = int(yf_num)
  dx = int(256.0*(xf_num-xtile))
  dy = int(256.0*(yf_num-ytile))
  pos_x = (xtile-xmin_idx)*256+dx
  pos_y = (ytile-ymin_idx)*255+dy
  return (pos_x, pos_y)

def getImageCluster(lat_deg, lon_deg, delta_lat,  delta_lon, zoom):
    xmin, ymax, in_x, in_y =deg2num(lat_deg - delta_lat, lon_deg - delta_lon, zoom)
    xmax, ymin, in_x, in_y =deg2num(lat_deg + delta_lat, lon_deg + delta_lon, zoom)
    Cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) ) 
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin,  ymax+1):
            img_path = "tiles/%d/%d/%d.png" % (zoom, xtile, ytile)
            if (os.path.isfile(img_path)):
                tile = Image.open(img_path)
                Cluster.paste(tile, box=((xtile-xmin)*256 ,  (ytile-ymin)*255))
            else: 
                print("Couldn't download image")
                tile = None
    r_img = Image.fromarray(np.asarray(Cluster))
    r_img = r_img.convert("RGBA")
    return r_img


def getGeojsonPolyImage(img_size,lat_deg, lon_deg, delta_lat, delta_lon,zoom,geojson_file):
    with open(geojson_file, encoding="utf-8") as json_file: #file not found
        json_data = json.load(json_file)
    xmin_idx,ymin_idx,xpos,ypos = deg2num(lat_deg+delta_lat,lon_deg-delta_lon, zoom)
    v_arry = json_data['features']
    v_img = Image.new('RGBA', img_size, (255,0,0,0) )
    v_draw = ImageDraw.Draw(v_img)
    for one_v in v_arry:
        vpoly = one_v['geometry']
        if vpoly['type'] == 'Polygon':
            ppts_arr = vpoly['coordinates']
            for prt_arr in ppts_arr:
                ptcnt = len(prt_arr)
                pts_arr = []
                for i in range(ptcnt):
                    pt_x,pt_y =  deg2posXY(xmin_idx,ymin_idx,prt_arr[i][1],prt_arr[i][0],zoom)
                    pts_arr.append((pt_x,pt_y))
                v_draw.polygon(pts_arr,fill=TINT_COLOR+(OPACITY,),outline=BLUE)
    return v_img

def main():
    zlevel = 14
    ntp_midx = 121.6381184
    ntp_midy = 24.9731632
    half_x = 0.368
    half_y = 0.325
    
    NTPvillageGeojson_file = 'new_taipei.geojson'
    back_img  = getImageCluster(ntp_midy, ntp_midx, half_y, half_x, zlevel)
    frnt_img  = getGeojsonPolyImage(back_img.size,ntp_midy, ntp_midx, half_y, half_x, zlevel,NTPvillageGeojson_file)
    result_img = Image.alpha_composite(back_img,frnt_img)
    result_img = result_img.convert("RGB")
    result_img.show()

if __name__ == '__main__':
    main()