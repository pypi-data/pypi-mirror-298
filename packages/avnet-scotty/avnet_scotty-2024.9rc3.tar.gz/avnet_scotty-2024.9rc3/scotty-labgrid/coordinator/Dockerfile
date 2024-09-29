# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"] 

RUN apt-get update
# Install git
RUN apt-get install git iproute2 nano net-tools nmap inetutils-ping curl -y
# Install what is necessary for the SDwire
RUN apt-get install build-essential libftdi1-dev libpopt-dev cmake pkg-config -y
# Install what is necessary for Labgrid
RUN apt-get install python3 python3-virtualenv python3-pip python3-setuptools virtualenv microcom libsnappy-dev ser2net -y 

# Install Labgrid
RUN virtualenv -p python3 /home/labgrid-venv
RUN source /home/labgrid-venv/bin/activate && pip install --upgrade pip
RUN source /home/labgrid-venv/bin/activate && cd /home && git clone -b stable-24.0 https://github.com/labgrid-project/labgrid
RUN source /home/labgrid-venv/bin/activate && cd /home/labgrid && pip install .

# Install coordinator 
RUN cd /home/labgrid && virtualenv -p python3 crossbar-venv
RUN cd /home/labgrid && crossbar-venv/bin/pip install --upgrade pip
RUN cd /home/labgrid && crossbar-venv/bin/pip install -r crossbar-requirements.txt
RUN cd /home/labgrid && virtualenv -p python3 labgrid-venv
RUN cd /home/labgrid && source /home/labgrid-venv/bin/activate && pip install --upgrade pip
RUN cd /home/labgrid && source /home/labgrid-venv/bin/activate && pip install .
RUN cd /home/labgrid && source /home/labgrid-venv/bin/activate && cp .crossbar/config-anonymous.yaml .crossbar/simpleswitch-coordinator.yaml
RUN cd /home/labgrid && source /home/labgrid-venv/bin/activate && sed -i "s#^  executable: .*\$#  executable: ${VIRTUAL_ENV}/bin/python3#" .crossbar/simpleswitch-coordinator.yaml
RUN IPaddress=$(hostname -I) && sed -i "s/172.17.0.3/$IPaddress/g" /home/labgrid/.crossbar/simpleswitch-coordinator.yaml
RUN sed -i "s/ :20408/:20408/g" /home/labgrid/.crossbar/simpleswitch-coordinator.yaml

# Install webserver
RUN cd /home && git clone https://github.com/sk3k-7535/labgrid-frontend-mle.git
RUN mkdir -p /home/labgrid/web
RUN cd /home/labgrid-frontend-mle/labgrid-web-client/dist/labgrid-web-client && cp * /home/labgrid/web
RUN cd /home/labgrid-frontend-mle/python-wamp-client && virtualenv -p python3 labby-venv
RUN cd /home/labgrid-frontend-mle/python-wamp-client && source labby-venv/bin/activate && pip install -r requirements.txt
RUN sed -i "s/DEFAULT_COORDINATOR = False/DEFAULT_COORDINATOR = True/g" /home/labgrid-frontend-mle/python-wamp-client/labby/labby.py

# Copy necessary script
RUN mkdir -p /home/labgrid-scripts
COPY coordinator.sh /home/labgrid-scripts

#Run the script
CMD /home/labgrid-scripts/coordinator.sh labby-venv/bin/activate && /bin/bash
