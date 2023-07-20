from gologin import GoLogin


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
        'mode': 'http', # Specify 'none' if not using proxy
        # 'autoProxyRegion': 'us',
        "host": '192.168.0.100',
        "port": '8080',
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