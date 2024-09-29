#!/bin/bash
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

cd coordinator || exit
docker build -t test-coordinator/labgrid-coordinator:1.0 .
docker run -it --name=coordinator -td -p 8083:8083 --rm --privileged test-coordinator/labgrid-coordinator:1.0
