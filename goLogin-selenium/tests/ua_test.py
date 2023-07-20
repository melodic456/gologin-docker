from fake_useragent import UserAgent

ua = UserAgent(browsers=['edge', 'chrome'])
user_agent = ua.random

print(user_agent)
if "Windows" in user_agent:
    print("windows")
elif "Macintosh" in user_agent:
    print("Mac")
elif "Linux" in user_agent:
    print("Linux")
elif "iPhone" in user_agent:
    print("iPhone")
