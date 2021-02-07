import json
import requests

def line_breaks(chars:str):
    ''' Returns string with a line break entered at defined interval '''

    chars = chars.split(" ")
    output = ""
    while chars:
        for word in chars[:8]:
            output += str(word) + " "
        output += "\n"
        chars = chars[8:]
    return output


def weather_api_call(lat:int, lon:int):
    ''' Returns json dictionary of weather data for assigned lat, lon coordinates '''
    
    # API call to fetch data related to assigned lat, lon coordinates
    api_call = f"https://api.weather.gov/points/{lat},{lon}"
    points_data = requests.get(api_call).json()
    
    who = points_data['properties']['gridId']
    x = points_data['properties']['gridX']
    y = points_data['properties']['gridY']
    
    # API call to fetch weather forecast data
    forecast_api = f"https://api.weather.gov/gridpoints/{who}/{x},{y}/forecast"
    output = requests.get(forecast_api).json()
    
    # Assign extra data to output
    raw_date = output['properties']['updated'][:10].split("-")
    output['date'] = f"{raw_date[1]}/{raw_date[2]}/{raw_date[0]}"
    output['city'] = points_data['properties']['relativeLocation']['properties']['city']
    output['state'] = points_data['properties']['relativeLocation']['properties']['state']
    return output

def main():
    while True:
        # Coordinates must be in the United States
        # No error checking currently exists for coordinates
        latitude = float(input("Latitude: "))
        longitude = float(input("Longitude: "))

        # Assign weather forecast data
        forecast = weather_api_call(latitude, longitude)

        # Display weather information for user
        banner = ("*" * 40 )
        print((banner + "\n") * 5)
        print(f"\nThe daily forecast for {forecast['city']}, {forecast['state']}")
        print(f"as of {forecast['date']}\n")
        for period in forecast['properties']['periods']:
            print( " " * (19 - (int(len(period['name'])/2))), period['name'])
            print(banner)
            print(line_breaks(period['detailedForecast']) + "\n")
            
if __name__ == "__main__":
    main()
