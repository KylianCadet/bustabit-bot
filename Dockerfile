FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
	software-properties-common \
	wget

# Firefox
RUN apt-get install -y firefox
ENV FIREFOX_VERSION 102.0
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
	&& rm -rf /opt/firefox \
	&& tar -C /opt -xf /tmp/firefox.tar.bz2 \
	&& rm /tmp/firefox.tar.bz2

# Geckodriver
ENV GECKODRIVER_VERSION 0.31.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
	&& rm -rf /opt/geckodriver \
	&& tar -C /opt -zxf /tmp/geckodriver.tar.gz \
	&& rm /tmp/geckodriver.tar.gz \
	&& mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
	&& chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
	&& ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver \
	&& ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires

# Python
RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip

# Install pip packages
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .