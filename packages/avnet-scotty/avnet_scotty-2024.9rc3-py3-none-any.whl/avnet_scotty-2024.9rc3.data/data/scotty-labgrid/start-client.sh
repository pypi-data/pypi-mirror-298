#!/bin/bash
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

cd client-"$1" || exit
docker build -t test-client/labgrid-client:1.0 .
docker run -it --name=client-"$1" -p "$2":20408 -p "$3":22 --rm --privileged -v /run/udev:/run/udev -v=/dev:/dev -v "$(dirname "${0}")"/../:/home/labgrid-results/ test-client/labgrid-client:1.0
