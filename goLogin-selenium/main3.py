import io
import json
import os
import time
import traceback
from datetime import datetime
from multiprocessing import Pool
from sys import platform

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from gologin import GoLogin


# from tests.create_profiles import create_profile, brower_get_main


# multiple

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


def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()


profile_id = ''

profile_ids = []
port_for_profile = 3500


def create_profile(ip, port, proxy_type):
    ua = UserAgent(browsers=['edge', 'chrome'])
    user_agent = ua.random
    os_name = ""
    platform_name = ""
    print(user_agent)

    if "Windows" in user_agent:
        os_name = "win"
        platform_name = "win32"
    elif "Macintosh" in user_agent:
        os_name = "mac"
        platform_name = "darwin"
    elif "Linux" in user_agent or "X11":
        os_name = "lin"
        platform_name = "linux"
    elif "iPhone" in user_agent:
        os_name = "iph"
        platform_name = "darwin"
    elif "Android" in user_agent:
        os_name = "and"
        platform_name = "linux"
    else:
        os_name = "lin"
        platform_name = "linux"

    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
    })

    profile_id = gl.create({
        "name": 'profile_mac',
        "os": str(os_name),
        "navigator": {
            "language": 'en-US',
            "userAgent": user_agent,
            "resolution": '1024x768',
            "platform": str(platform_name),
        },
        'proxy': {
            'mode': str(proxy_type),  # Specify 'none' if not using proxy
            # 'autoProxyRegion': 'us',
            "host": str(ip),
            "port": str(port),
            "username": '',
            "password": '',
        },
        "webRTC": {
            "mode": "alerted",
            "enabled": True,
        },
    });

    print('profile id=', profile_id);

    # gl.update({
    #     "id": 'yU0Pr0f1leiD',
    #     "name": 'profile_mac2',
    # });

    profile = gl.getProfile(profile_id);

    print('new profile name=', profile.get("name"));

    # gl.delete(profile_id)
    return profile_id


def brower_get_main(profile):
    print("---------------------------browser get main started-----------------------")
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
        'profile_id': profile['profile_id'],
        'port': profile['port'],
    })

    if platform == "linux" or platform == "linux2":
        chrome_driver_path = "./chromedriver"
    elif platform == "darwin":
        chrome_driver_path = "./mac/chromedriver"
    elif platform == "win32":
        chrome_driver_path = f"F:\python\goLogin-selenium\chromedriver.exe"

    debugger_address = gl.start()
    chrome_options = Options()
    # chrome_options.add_argument("--proxy-server=socks5://" + str(ip) + ":" + str(port))
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service(executable_path=chrome_driver_path)
    # driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get("http://deliv12.com/redirect?sid=101209")
    # assert "Python" in driver.title
    time.sleep(40)
    driver.quit()
    time.sleep(3)
    gl.stop()
    gl.delete(profile['profile_id'])


# with open("hide_ip_extracted.txt", "r") as f:
#     for line in f:
#         ip = line.split(":")[0]
#         port = line.split(":")[1]
#         port = port.split("\n")[0]
#         print(port)
#         profile_id_ = create_profile(ip, port)
#         # profile_ids.append(profile_id_)
#         profile_ids.append({'profile_id': str(profile_id_), 'port': port_for_profile})
#         port_for_profile = port_for_profile + 1

id_list = []

print("------------------------------Browser Making Done----------------------------")
print(profile_ids)
print("------------------------------Browser get Start----------------------------")

if __name__ == '__main__':
    for i in range(5):
        try:
            id = ""
            list_proxies = get_valid_proxy_list("?used_time=0&status=online&order_by=-last_checked")
            if list_proxies == "error" or len(list_proxies) < 1:
                exit(0)
            else:
                id = list_proxies[0]["id"]
            proxy, proxy_type = get_proxy_by_id(id)
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
            profile_id_ = create_profile(ip, port, proxy_type)
            update_proxy(id, data={"used_time": "using"})
            id_list.append(id)
            # profile_ids.append(profile_id_)
            profile_ids.append({'profile_id': str(profile_id_), 'port': port_for_profile})
            port_for_profile = port_for_profile + 1
        except:
            pass
    with Pool(2) as p:
        p.map(brower_get_main, profile_ids)

    for id in id_list:
        now = datetime.now()
        print(now)
        update_proxy(id, data={"used_time": str(now)})

    if platform == "win32":
        os.system('taskkill /im chrome.exe /f')
        os.system('taskkill /im chromedriver.exe /f')
    else:
        os.system('killall -9 chrome')
        os.system('killall -9 chromedriver')
# for pro
#         try:
#
#             gl = GoLogin({
#                 "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
#                 })
#
#             profile_id = gl.create({
#                 "name": 'profile_mac',
#                 "os": 'mac',
#                 "navigator": {
#                     "language": 'en-US',
#                     "userAgent": 'random',
#                     "resolution": '1024x768',
#                     "platform": 'mac',
#                 },
#                 'proxy': {
#                     'mode': 'socks5', # Specify 'none' if not using proxy
#                     # 'autoProxyRegion': 'us',
#                     "host": str(ip),
#                     "port": str(port),
#                     "username": '',
#                     "password": '',
#                 },
#                 "webRTC": {
#                     "mode": "alerted",
#                     "enabled": True,
#                 },
#             });
#
#             print('profile id=', profile_id);
#
#             # gl.update({
#             #     "id": 'yU0Pr0f1leiD',
#             #     "name": 'profile_mac2',
#             # });
#
#             profile = gl.getProfile(profile_id);
#
#             print('new profile name=', profile.get("name"));
#
#             # gl.delete('yU0Pr0f1leiD')
#
#
#
#
#             gl = GoLogin({
#                 "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
#                 "profile_id": str(profile_id)
#                 })
#
#             if platform == "linux" or platform == "linux2":
#                 chrome_driver_path = "./chromedriver"
#             elif platform == "darwin":
#                 chrome_driver_path = "./mac/chromedriver"
#             elif platform == "win32":
#                 chrome_driver_path = f"F:\python\goLogin-selenium\chromedriver.exe"
#
#
#
#             debugger_address = gl.start()
#             chrome_options = Options()
#             chrome_options.add_argument("--proxy-server=socks5://" + str(ip) + ":" + str(port))
#             chrome_options.add_experimental_option("debuggerAddress", debugger_address)
#             service = Service(executable_path=chrome_driver_path)
#             # driver = webdriver.Chrome(service=service)
#             driver = webdriver.Chrome(service=service, options=chrome_options)
#             # driver = webdriver.Chrome()
#             driver.get("http://deliv12.com/redirect?sid=101209")
#             # assert "Python" in driver.title
#             time.sleep(40)
#             driver.quit()
#             time.sleep(3)
#             gl.stop()
#             gl.delete(profile_id)
#         except Exception as ex:
#             print("there is an error")
#             error = get_exception_traceback_str(ex)
#             print(error)
#             gl.delete(profile_id)


# cscxz
