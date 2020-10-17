import json
import requests

url = 'http://127.0.0.1:5000/api/'
files = {'upload_file': open('myCsvFile.csv', 'rb')}


def post_request_example():
    with open("myCsvFile.csv", "rb") as csv_file:
        file_dict = {"csv_file": csv_file}
        response = requests.post(url + "getAddresses", files=file_dict)
        print(json.loads(response.text))


def get_request_example():
    payload = {'result_id': 'test', 'key2': 'value2'}
    response = requests.get(url + "getResult", params=payload)
    print(json.loads(response.text))


if __name__ == '__main__':
    post_request_example()
    get_request_example()