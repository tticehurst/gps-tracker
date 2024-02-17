from requests import request
from json import loads
from glob import glob
from os import path
from dotenv import load_dotenv
from datetime import datetime

from db import query

load_dotenv()

files = glob(path.join("geojson", "*.geojson"))

for file in files:
    fileData = loads(open(file, "r").read())

    for feature in fileData["features"]:

        (time, lat, lon) = (
            datetime.strptime(feature["properties"]["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            feature["geometry"]["coordinates"][1],
            feature["geometry"]["coordinates"][0],
        )

        doesExist = query("SELECT 1 FROM readings WHERE reading_time = %s", [time])

        if not doesExist:
            responseInfo = request(
                "GET",
                f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1",
            ).json()

            print(
                f"Time: {time} | Lon: {lon}, Lat: {lat} | Address: {responseInfo['display_name']}"
            )

            query(
                "INSERT INTO readings (reading_time,lat,lon,geoloc) VALUES (%s,%s,%s,%s)",
                [time, lat, lon, responseInfo["display_name"]],
                True,
            )
        else:
            print(f"Time: {time} | Lon: {lon}, Lat: {lat} | !Already exists!")
