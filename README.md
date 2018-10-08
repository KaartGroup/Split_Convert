# Split Convert Tool
A tool to split a .shp file into multiple .osm.pbf files using a given aera (meters) and a given translation file.

## Installation
    Python 2.7.x
    Osmosis

### Installing on OSX
#### Osmosis
Follow the instructions [here](https://wiki.openstreetmap.org/wiki/Osmosis#Latest_stable_version) to install Osmosis.

#### Python Requirements
To install the necessary python requirements, run the following from the root project directory:

    pip install -r requirements.txt

### Usage
    usage: split_convert.py [-h] [-a AREA_SIZE] [-t TRANSLATION] file

    Split one .shp file into multiple .osm.pbf files using a given area(meters) and a given translation file

    positional arguments:
    file                  .shp file you wish to split and convert

    optional arguments:
    -h, --help            show this help message and exit
    -a AREA_SIZE, --area_size AREA_SIZE
                            size in meters to split the .shp file into
    -t TRANSLATION, --translation TRANSLATION
                            Select the attribute-tags translation
                            method. Must follow the standard for
                            ogr2osm.