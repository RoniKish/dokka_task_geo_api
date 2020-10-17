from math import sin, cos, sqrt, atan2, radians
import requests
import json

from flask import Flask, request, jsonify
import pymongo
import pandas as pd

app = Flask(__name__)
mongo_db_ip = "localhost"
mongo_db_port = "27017"


@app.route('/api/getAddresses', methods=['POST'])
def getAddresses():
    points = []
    links = []
    file = request.files['csv_file']
    data = pd.read_csv(file, float_precision='round_trip')
    for index, row in data.iterrows():
        name = row['Point']
        latitude = row['Latitude']
        longitude = row['Longitude']
        point_address = get_point_address(latitude, longitude)
        if point_address:
            points.append({"name": name, "address": point_address})
            links += get_all_distances_of_first_row(data[index:])
    _id = insert_points_and_links_to_db(points, links)
    return jsonify({"points": points, "links": links, "result_id": str(_id)})


@app.route('/api/getResult', methods=['GET'])
def getResult():
    result_id = request.args.get('result_id')
    result_cursor = get_points_and_links_from_db(result_id)
    result_list = list(result_cursor)
    return jsonify(result_list[0])


def get_points_and_links_from_db(result_id):
    points_and_links_collection = get_points_and_links_collection("dokka_db")
    return points_and_links_collection.find({"_id": result_id})


def get_point_address(latitude, longitude):
    base_url_prefix = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location='
    base_url_suffix = '&langCode=en&outSR=&forStorage=false&f=pjson'
    try:
        r = requests.get(base_url_prefix + str(latitude) + '%2C' + str(longitude) + base_url_suffix)
        json_reader = json.loads(r.text)
        if 'error' in json_reader:
            return None
        return json_reader['address']['Match_addr']
    except Exception as e:
        return None


def get_all_distances_of_first_row(data):
    distances = []
    first_row_name = data.iloc[0]['Point']
    first_row_point = [data.iloc[0]['Latitude'], data.iloc[0]['Longitude']]
    for index, row in data[1:].iterrows():
        name = first_row_name + row['Point']
        point = [row['Latitude'], row['Longitude']]
        distance = get_distance_from_lat_lon_in_km(first_row_point, point)
        distances.append({"name": name, "distance": distance})
    return distances


def get_distance_from_lat_lon_in_km(point_1, point_2):
    # approximate radius of earth in km
    R = 6373.0

    lat_1, lon_1 = radians(point_1[0]), radians(point_1[1])
    lat_2, lon_2 = radians(point_2[0]), radians(point_2[1])
    lat_distance = lat_2 - lat_1
    lon_distance = lon_2 - lon_1

    a = sin(lat_distance / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(lon_distance / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance * 1000


def insert_points_and_links_to_db(points, links):
    points_and_links_collection = get_points_and_links_collection("dokka_db")
    _id = points_and_links_collection.insert_one({"points": points, "links": links})
    return str(_id.inserted_id)


def get_points_and_links_collection(db_name):
    my_client = pymongo.MongoClient("mongodb://" + mongo_db_ip + ":" + mongo_db_port)
    dokka_db = my_client[db_name]
    return dokka_db["pointsAndLinks"]


if __name__ == '__main__':
    app.run()
