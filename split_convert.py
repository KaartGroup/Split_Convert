#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' split_convert

This program will split a given OGR understandable file into individual files of a given area. It will then, using ogr2osm convert the individual squares into OSM PBF files. 

To use, submit 

Copyright (c) 2018 Kaart Group <admin@kaartgroup.com>

Released under the MIT license: http://opensource.org/licenses/mit-license.php

'''

from shapely.geometry import Polygon, mapping, shape
import numpy as np
import fiona
import os
import argparse
import subprocess
import shutil

''' Set up the arguments '''
parser = argparse.ArgumentParser(description="Split one .shp file into multiple .osm.pbf files using a given area(meters) and a given translation file")
parser.add_argument('file', help=".shp file you wish to split and convert")
parser.add_argument('-a','--area_size', help="size in meters to split the .shp file into", type=float)
parser.add_argument('-t','--translation', help='Select the attribute-tags translation method. Must follow the standard for ogr2osm.')
args = parser.parse_args()

''' Create the new directories for the file '''
parentDir = os.path.abspath(os.path.join(args.file, os.pardir))
newDir = os.path.join(parentDir, args.file.split('/')[-1].replace('.shp', ''))
if os.path.exists(newDir):
    shutil.rmtree(newDir)
os.makedirs(newDir)
os.makedirs(os.path.join(newDir, "Cygnus_Outputs"))


def createGrid(file):
    ''' Create a new .shp file of a grid around the 
    data of the given file '''

    with fiona.open(file,'r') as d:
        xmin, ymin, xmax, ymax = d.bounds
        gridWidth = args.area_size
        gridHeight = args.area_size
        rows = (ymax-ymin)/gridHeight
        cols = (xmax-xmin)/gridWidth
        ringXleftOrigin = xmin
        ringXrightOrigin = xmin + gridWidth
        ringYtopOrigin = ymax
        ringYbottomOrigin = ymax-gridHeight
        schema = {'geometry': 'Polygon','properties': {'grid': 'int'}}
        id = 1
        recs = []
        for i in np.arange(cols):
                ringYtop = ringYtopOrigin
                ringYbottom = ringYbottomOrigin
                for j in np.arange(rows):
                    polygon = Polygon([(ringXleftOrigin, ringYtop), (ringXrightOrigin, ringYtop), (ringXrightOrigin, ringYbottom), (ringXleftOrigin, ringYbottom)])
                    ds = list(d.items(bbox=polygon.bounds))
                    # check if there is any file data in the grid
                    if len(ds) > 0:
                        recs.append({'geometry': mapping(polygon), 'properties': {'grid': id}})
                        id += 1
                    ringYtop = ringYtop - gridHeight
                    ringYbottom = ringYbottom - gridHeight
                ringXleftOrigin = ringXleftOrigin + gridWidth
                ringXrightOrigin = ringXrightOrigin + gridWidth
        with fiona.open(os.path.join(newDir, 'grid.shp'), 'w', d.driver, schema, d.crs) as g:
            g.writerecords(recs)


def joinLayers(file):
    ''' Do a spatial join of the original file with the grid to get individual squares as .shp '''
    with fiona.open(os.path.join(newDir, 'grid.shp'), 'r') as g:
        with fiona.open(file, 'r') as r:
            for grid in g:
                name = "/square_"+str(grid['properties']['grid'])
                dir = os.path.join(newDir + name)
                if os.path.exists(dir):
                    shutil.rmtree(dir)
                else:
                    os.makedirs(dir)
                with fiona.open(dir + name + ".shp", 'w', r.driver, r.schema, r.crs) as joined:
                    roads = r.items(bbox=shape(grid['geometry']).bounds)
                    for road in roads:
                        joined.write({
                                'properties': road[1]['properties'],
                                'geometry': road[1]['geometry']
                            })


def shape2osm(file, translation):
    ''' Convert given .shp file to .osm.pbf file '''
    name = file.split('/')[-1].replace('.shp', '')
    dir = os.path.join(newDir, name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    ogr = "python ogr2osm/ogr2osm.py -t \"" + translation + "\" \"" + file + "\" -o \"" + os.path.join(dir, name) + ".osm\" --add-version --positive-id"
    osmosis = "osmosis --read-xml \"" + os.path.join(dir, name) + ".osm\" enableDateParsing=no --write-pbf \"" + os.path.join(dir, name) + ".osm.pbf\" omitmetadata=true"
    subprocess.call(ogr, shell=True)
    subprocess.call(osmosis, shell=True)


if __name__ == "__main__":
    createGrid(args.file)
    joinLayers(args.file)
    for root, dirs, files in os.walk(newDir):
        for dir in dirs:
            for f in os.listdir(os.path.join(root, dir)):
                if f.endswith('.shp'):
                    print os.path.join(root, dir, f)
                    shape2osm(os.path.join(root, dir, f), args.translation)
