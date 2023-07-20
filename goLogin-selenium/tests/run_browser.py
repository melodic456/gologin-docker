import time
import os
from multiprocessing import Pool
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from gologin import GoLogin

def scrap(profile):
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
    chrome_options.add_argument("--proxy-server=socks5://" + str(ip) + ":" + str(port))
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
    gl.delete(profiles['profile_id'])

profiles = [
	{'profile_id': 'profile_id_1', 'port': 3500},
	{'profile_id': 'profile_id_2', 'port': 3501},
	{'profile_id': 'profile_id_3', 'port': 3502},
	]


with Pool(3) as p:
	p.map(scrap, profiles)


if platform == "win32":
	os.system('taskkill /im chrome.exe /f')
	os.system('taskkill /im chromedriver.exe /f')
else:
	os.system('killall -9 chrome')
	os.system('killall -9 chromedriver')
