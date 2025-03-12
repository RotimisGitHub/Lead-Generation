import json
from pprint import pprint

import requests

api_key = "AIzaSyCJTqm2sCmACz3xtK-scFguw1LzcxLJRww"


def get_coordinates(api_key, city):
    """
        Retrieves the coordinates (longitude, latitude) of the chosen business using the Google Places API.

        Parameters:
        - chosen_business (str): The name of the chosen business.
        - api_key (str): The API key for accessing the Google Places API.

        Returns:
        - tuple: A tuple containing the longitude and latitude of the chosen business.
        """

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    payload = {
        "input": city,
        "inputtype": "textquery",
        "fields": "geometry",
        "key": api_key,
    }

    response = requests.get(url, params=payload)
    data_ = response.json()

    northeast_longitude = data_['candidates'][0]['geometry']['viewport']['northeast']['lng']
    northeast_latitude = data_['candidates'][0]['geometry']['viewport']['northeast']['lat']
    southwest_longitude = data_['candidates'][0]['geometry']['viewport']['southwest']['lng']
    southwest_latitude = data_['candidates'][0]['geometry']['viewport']['southwest']['lat']

    coordinates = {
        'northeast_longitude': northeast_longitude,
        'northeast_latitude': northeast_latitude,
        'southwest_longitude': southwest_longitude,
        'southwest_latitude': southwest_latitude,
    }

    return coordinates


def section_city(divider, city):
    city = get_coordinates(api_key, city)

    latitude_min = city['southwest_latitude']
    longitude_min = city['southwest_longitude']
    latitude_max = city['northeast_latitude']
    longitude_max = city['northeast_longitude']

    lat_step = (latitude_max - latitude_min) / divider
    lng_step = (longitude_max - longitude_min) / divider

    grid_coordinates = []

    for row in range(divider):
        for column in range(divider):
            # Calculate the coordinates for the current grid cell
            cell_lat_min = latitude_min + row * lat_step
            cell_lat_max = latitude_min + (row + 1) * lat_step
            cell_lng_min = longitude_min + column * lng_step
            cell_lng_max = longitude_min + (column + 1) * lng_step

            # Append the coordinates of the current grid cell to the list
            grid_coordinates.append({"ranges": {
                'latitude_min': cell_lat_min,
                'latitude_max': cell_lat_max,
                'longitude_min': cell_lng_min,
                'longitude_max': cell_lng_max
            },

                "Midpoints": {
                    "Latitude": (cell_lat_max + cell_lat_min) / 2,
                    "Longitude": (cell_lng_max + cell_lng_min) / 2,

                }

            })

    # for idx, cell in enumerate(grid_coordinates):
    #     print(f"Grid Cell {idx + 1}:")
    #     print(f"Latitude Range: {cell['latitude_min']} to {cell['latitude_max']}")
    #     print(f"Longitude Range: {cell['longitude_min']} to {cell['longitude_max']}")
    #     print()

    return grid_coordinates
