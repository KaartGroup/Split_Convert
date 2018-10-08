# Split Convert Tool
A tool to split a .shp file into multiple .osm.pbf files using a given aera (meters) and a given translation file.

## Installation
### Requirements
    Python 2.7.x
    Osmosis

### Installing on OSX
#### Osmosis
Follow the instructions [here](https://wiki.openstreetmap.org/wiki/Osmosis#Latest_stable_version) to install Osmosis.

#### Python Requirements
To install the necessary python requirements, run the following from the root project directory:

    pip install -r requirements.txt

### About
This tool was developed to help automate the processes needed to prepare government supplied Shapefiles for an OSM import. It is intended to create file suitable to be run through Telenav's [Cygnus](http://blog.improveosm.org/en/tag/cygnus/) conflation tool that requires files to be less than 50km x 50km.

The `inegi_mgn.py` file is specific to an import here at Kaart but is a simple example of a translation file. More examples can be seen in the `ogr2osm/translations` directory.

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