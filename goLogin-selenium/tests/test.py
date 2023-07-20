import json
import time
from datetime import datetime

import requests


def request_for_django_api(path="", method="GET", data=None):
    # url = self.ApiUrl + path
    url = "http://localhost:8000/api/v1/proxymodel/" + path
    # timestamp = str(int(datetime.datetime.now().timestamp()))
    # valueToEncode = self.api_key + ":" + method + ":" + path + ":" + str(timestamp)
    # token = self.create_token(valueToEncode, self.api_secret)
    headers = {"Content-Type": "application/json"}
    # if OtohitsRequest.Credentials:
    # token = self.CreateToken()
    # headers["Authorization"] = "otoapi " + valueToEncode + ":" + token
    print(headers)
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == "PATCH":
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError("Invalid HTTP method")
    # response.raise_for_status()
    print(response)
    return response


def get_all_list(order_by="used_time"):
    response = request_for_django_api("?order_by=" + order_by, method="GET").json()
    return response["objects"]


def get_valid_proxy_list(query=""):
    response = request_for_django_api(query, method="GET").json()
    try:
        if response["error"]:
            return "error"
    except:
        pass
    return response["objects"]


def get_proxy_by_id(id):
    response = request_for_django_api(str(id) + "/").json()
    proxies = response["ip"] + ":" + response["port"]
    proxy_type = response["type"]
    print(proxies)
    return proxies, proxy_type


def update_proxy(id, data):
    response = request_for_django_api(str(id) + "/", method="PATCH", data=data)


# data = {"ip": "10", "last_checked": "10", "port": "1", "status": "1", "type": "1", "used_time": "1"}
# data = {"ip": "20"}
#
# # response = request_for_django_api("1/", method="PATCH", data=data)
# # # response = request_for_django_api("1", method="GET")
# # print(response)
#
# # get ip with check
# # http://127.0.0.1:8000/api/v1/proxymodel/?order_by=used_time
# response = request_for_django_api("?order_by=used_time", method="GET")
#
# objects = response.json()["objects"]
# used = objects[0]["used_time"]
# # print(objects[0]["used_time"])
# if used == "0":
#     response = request_for_django_api(str(objects[0]["id"]) + "/").json()
#     proxies = response["ip"] + ":" + response["port"]
#     print(proxies)


# get a valid proxy
# list_proxies = get_all_list()
id = ""
list_proxies = get_valid_proxy_list("?used_time=0&status=online&order_by=-last_checked")
if list_proxies == "error" or len(list_proxies) < 1:
    exit(0)
else:
    id = list_proxies[0]["id"]
proxy, proxy_type = get_proxy_by_id(id)
# use it in the browser
# update db with used_time=using
update_proxy(id, data={"used_time": "using"})
# update db with used_time=datetime
time.sleep(5)
now = datetime.now()
print(now)
update_proxy(id, data={"used_time": str(now)})
