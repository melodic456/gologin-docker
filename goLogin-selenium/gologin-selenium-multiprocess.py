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
	        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M',
	        'profile_id': profile['profile_id'],
	        'port': profile['port'],
		})

	if platform == "linux" or platform == "linux2":
		chrome_driver_path = './chromedriver'
	elif platform == "darwin":
		chrome_driver_path = './mac/chromedriver'
	elif platform == "win32":
		chrome_driver_path = f"F:\python\goLogin-selenium\chromedriver.exe"

	debugger_address = gl.start()
	chrome_options = Options()
	chrome_options.add_experimental_option("debuggerAddress", debugger_address)
	service = Service(executable_path=chrome_driver_path)
	# driver = webdriver.Chrome(service=service)
	driver = webdriver.Chrome(service=service, options=chrome_options)
	driver.get("http://www.python.org")
	print('ready', profile['profile_id'], driver.title)
	time.sleep(10)
	print('closing', profile['profile_id'])
	driver.quit()
	time.sleep(3)
	gl.stop()

profiles = [
	{'profile_id': '64b722e6a8bb2cfec15ccc0c', 'port': 3500},
	{'profile_id': '64b722e5b96715b047d18839', 'port': 3501},
	{'profile_id': '64b722e4da509cc11b97a9eb', 'port': 3502},
	]



if __name__ == '__main__':
	with Pool(3) as p:
		p.map(scrap, profiles)


	if platform == "win32":
		os.system('taskkill /im chrome.exe /f')
		os.system('taskkill /im chromedriver.exe /f')
	else:
		os.system('killall -9 chrome')
		os.system('killall -9 chromedriver')
