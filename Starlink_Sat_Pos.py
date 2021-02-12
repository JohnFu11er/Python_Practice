import requests
import json

'''
    Filename: Starlink_Sat_Pos.py
    Author: John Fuller
    Date created: 2/10/2021
    Date last modified: 2/10/2021
    Description:
        Generates KML file containing the Name, latitude, longitude,
        and altitude for all satellite vehicles in the Starlink 
        constellation.
'''

# API source call
sat_data = requests.get("https://api.spacexdata.com/v4/starlink").json()

# Save location of kml file
filename = "starlink_position.kml"

def my_data(data):
    ''' Returns structured data that only includes
    Name, Lat, Long, and Altitude'''
    output = {}
    for sat in data:
        output[sat['spaceTrack']['OBJECT_NAME']] = {}
        output[sat['spaceTrack']['OBJECT_NAME']]['latitude'] = sat['latitude']
        output[sat['spaceTrack']['OBJECT_NAME']]['longitude'] = sat['longitude']
        output[sat['spaceTrack']['OBJECT_NAME']]['height_km'] = sat['height_km']
    return output


def main():
    ''' Constructs the KML data file '''
    header()
    get_starlink_data(my_data(sat_data))
    footer()

def header():
    ''' Initializes the .kml file and writes the opening section of the .kml file '''
    with open(filename, mode='wt', newline='') as _iss:
            _iss.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            _iss.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            _iss.write('  <Document>\n')

def get_starlink_data(starlink_data):
    ''' Creates a point in the KML file for each
    Starlink satellite vehicle retrived in the 
    API call '''
    for satellite, values in starlink_data.items():
        if values['longitude'] != None:
            with open(filename, mode='at', newline='') as _iss:
                _iss.write('    <Placemark>\n')
                _iss.write(f'      <name>{satellite.split("-")[1]}</name>\n')
                _iss.write('      <Point>\n')
                _iss.write(f'        <coordinates>{values["longitude"]},{values["latitude"]},{values["height_km"]*1000}</coordinates>\n')
                _iss.write('         <altitudeMode>absolute</altitudeMode>\n')
                _iss.write('      </Point>\n')
                _iss.write('    </Placemark>\n')


def footer():
    ''' Appends the required end of the .kml file '''
    with open(filename, mode='at', newline='') as _iss:
            _iss.write('  </Document>\n')
            _iss.write('</kml>\n')

if __name__ == "__main__":
    main()
