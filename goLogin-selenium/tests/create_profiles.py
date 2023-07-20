from gologin import GoLogin
from fake_useragent import UserAgent
import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
def create_profile(ip, port):
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