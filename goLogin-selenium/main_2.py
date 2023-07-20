import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from gologin import GoLogin
from gologin import getRandomPort
import io
import traceback



# multiple

def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()

profile_id = ''

profile_ids = []

with open("hide_ip_extracted.txt", "r") as f:

    for line in f:
        ip = line.split(":")[0]
        port = line.split(":")[1]
        # profile_id_ = create_profile(ip, port)
        # profile_ids.append(profile_id_)
        try:

            gl = GoLogin({
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
                })

            profile_id = gl.create({
                "name": 'profile_mac',
                "os": 'mac',
                "navigator": {
                    "language": 'en-US',
                    "userAgent": 'random',
                    "resolution": '1024x768',
                    "platform": 'mac',
                },
                'proxy': {
                    'mode': 'socks5', # Specify 'none' if not using proxy
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

            # gl.delete('yU0Pr0f1leiD')




            gl = GoLogin({
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M",
                "profile_id": str(profile_id)
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
            gl.delete(profile_id)
        except Exception as ex:
            print("there is an error")
            error = get_exception_traceback_str(ex)
            print(error)
            gl.delete(profile_id)


