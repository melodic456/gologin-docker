FROM ubuntu:20.04
LABEL authors="melo"
#install python3-pip
USER root

# Install vnc, xvfb in order to create a 'fake' display and chrome
RUN 	export DEBIAN_FRONTEND=noninteractive
RUN 	export DISPLAY=0

RUN 	ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime

RUN 	apt-get update &&\
	 	apt-get install -y tzdata &&\
	 	dpkg-reconfigure --frontend noninteractive tzdata &&\
	 	apt-get install -y x11vnc xvfb zip wget curl psmisc supervisor gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-bin libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libgbm-dev nginx libcurl3-gnutls python3-pip


#add orbita browser in .gologin
RUN mkdir -p /root/.gologin/browser
# GOLOGIN INSTALL
COPY orbita-browser-latest.tar.gz /root/

RUN tar -xzf /root/orbita-browser-latest.tar.gz -C /root/.gologin/browser

# chmod 4755 chrome-sandbox
RUN chmod 4755 /root/.gologin/browser/orbita-browser/chrome-sandbox

# add script files
COPY goLogin-selenium /root/goLogin-selenium

RUN pip3 install -r /root/goLogin-selenium/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN	 chmod 777 /entrypoint.sh \
	&& mkdir /tmp/.X11-unix \
	&& chmod 1777 /tmp/.X11-unix

ENTRYPOINT ["/entrypoint.sh"]