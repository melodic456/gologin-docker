import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from gologin import GoLogin
from gologin import getRandomPort


gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
	"profile_id": "64b6bcf5d80b5441c0fb89bd"
	})

if platform == "linux" or platform == "linux2":
	chrome_driver_path = "./chromedriver"
elif platform == "darwin":
	chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
	chrome_driver_path = f"F:\python\goLogin-selenium\chromedriver.exe"



debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
service = Service(executable_path=chrome_driver_path)
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(service=service, options=chrome_options)
# driver = webdriver.Chrome()
driver.get("http://deliv12.com/redirect?sid=101209")
# assert "Python" in driver.title
time.sleep(20)
driver.quit()
time.sleep(3)
gl.stop()
