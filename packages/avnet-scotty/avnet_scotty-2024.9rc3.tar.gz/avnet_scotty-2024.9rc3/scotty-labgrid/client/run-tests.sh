#!/bin/bash
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# shellcheck source=/dev/null

/home/labgrid-scripts/generate-ssh-key.sh "$1"
source "$4" && labgrid-exporter -x ws://"$2":20408/ws /home/labgrid-files/exporter-"$3".yaml &
sleep 5
value=$(source "$4" && labgrid-client -x ws://"$2":20408/ws resources)
source "$4" && labgrid-client -x ws://"$2":20408/ws -p place-"$3" create
while IFS= read -r line; do
    if [[ $line == *$3* ]]; then
        source "$4" && labgrid-client -x ws://"$2":20408/ws -p place-"$3" add-match "$line"
    fi
done <<< "$value"
source "$4" && labgrid-client -x ws://"$2":20408/ws -p place-"$3" acquire

source "$4" && cd /home/testsuite && pytest --lg-env /home/labgrid-files/env-"$3".yaml --lg-coordinator=ws://"$2":20408/ws --lg-log --lg-colored-steps -vvv -s
