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
            print(
                f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
            )
            print(lat, lon)
            responseInfo = request(
                "GET",
                f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
                    "referer": "https://nominatim.openstreetmap.org/",
                },
            ).json()

            print(
                f"Time: {time} | Lon: {lon}, Lat: {lat} | {responseInfo['display_name']}"
            )

            query(
                "INSERT INTO readings (reading_time,lat,lon,geoloc) VALUES (%s,%s,%s,%s)",
                [time, lat, lon, responseInfo["display_name"]],
                True,
            )
        # else:
        #     print(f"Time: {time} | Lon: {lon}, Lat: {lat} | !Already exists!")
