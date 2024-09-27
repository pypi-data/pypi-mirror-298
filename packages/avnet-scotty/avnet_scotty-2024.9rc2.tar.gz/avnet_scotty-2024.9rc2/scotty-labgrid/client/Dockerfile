# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"] 

RUN apt-get update
# Install git
RUN apt-get install git iproute2 nano net-tools nmap inetutils-ping openssh-server debconf-utils mosquitto -y
# Install what is necessary for the SDwire
RUN apt-get install build-essential libftdi1-dev libpopt-dev cmake pkg-config -y
# Install what is necessary for Labgrid
RUN apt-get install python3 python3-virtualenv python3-pip python3-setuptools virtualenv microcom libsnappy-dev ser2net -y 

# Install expect
RUN echo 'tzdata tzdata/Areas select Europe' | debconf-set-selections
RUN echo 'tzdata tzdata/Zones/Europe select Paris' | debconf-set-selections
RUN DEBIAN_FRONTEND="noninteractive" apt install -y tzdata
RUN apt-get update
RUN apt-get install expect -y

# Install the SDWire tool
RUN mkdir -p /home/sdwire
RUN cd /home/sdwire && git clone https://github.com/Badger-Embedded/badgerd-sdwirec.git
RUN cd /home/sdwire/badgerd-sdwirec/sdwirec-sw && mkdir build
RUN cd /home/sdwire/badgerd-sdwirec/sdwirec-sw/build && cmake ..
RUN cd /home/sdwire/badgerd-sdwirec/sdwirec-sw/build && make
RUN cd /home/sdwire/badgerd-sdwirec/sdwirec-sw/build && make install

# Install Labgrid
RUN virtualenv -p python3 /home/labgrid-venv
RUN source /home/labgrid-venv/bin/activate && pip install --upgrade pip
RUN source /home/labgrid-venv/bin/activate && cd /home && git clone -b stable-24.0 https://github.com/labgrid-project/labgrid
RUN source /home/labgrid-venv/bin/activate && cd /home/labgrid && pip install .

# Install mqtt library for the tasmota plug
RUN source /home/labgrid-venv/bin/activate && pip install paho-mqtt

# Install library for the gpio expander
RUN source /home/labgrid-venv/bin/activate && pip install numato-gpio

# Install library for the tests reports
RUN source /home/labgrid-venv/bin/activate && pip install pytest-reportlog

# Add a password to user root
RUN echo 'root:root' | chpasswd

# Copy necessary scripts
RUN mkdir -p /home/labgrid-scripts
COPY generate-ssh-key.sh /home/labgrid-scripts
COPY interactive-ssh-copy-id.sh /home/labgrid-scripts
COPY run-tests.sh /home/labgrid-scripts
COPY release-place.sh /home/labgrid-scripts

# Copy necessary files
RUN mkdir -p /home/labgrid-files
COPY gpioexpanderdriver.py /home/labgrid-files/gpioexpanderdriver.py
COPY simpleswitchstrategy.py /home/labgrid-files/simpleswitchstrategy.py
COPY exporter-sm2s-imx8nano.yaml /home/labgrid-files/
COPY env-sm2s-imx8nano.yaml /home/labgrid-files/
COPY exporter-sm2s-imx8plus.yaml /home/labgrid-files/
COPY env-sm2s-imx8plus.yaml /home/labgrid-files/
COPY exporter-sm2s-intel-all.yaml /home/labgrid-files/
COPY env-sm2s-intel-all.yaml /home/labgrid-files/

# Create a directory for the ip results
RUN mkdir -p /home/labgrid-results

# Copy the testsuite
COPY testsuite /home/testsuite

