#!/bin/bash
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# shellcheck source=/dev/null

cd /home/labgrid && crossbar-venv/bin/crossbar start --config simpleswitch-coordinator.yaml &

sleep 5

cd /home/labgrid-frontend-mle/python-wamp-client && source "$1" && python -m labby --backend_url ws://172.17.0.2:20408/ws &
