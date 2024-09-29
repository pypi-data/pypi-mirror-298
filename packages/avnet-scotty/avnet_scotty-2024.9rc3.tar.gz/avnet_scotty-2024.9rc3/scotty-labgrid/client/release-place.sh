#!/bin/bash
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# shellcheck source=/dev/null

source "$3" && labgrid-client -x ws://"$1":20408/ws -p place-"$2" unlock

source "$3" && labgrid-client -x ws://"$1":20408/ws -p place-"$2" delete

places=$(source "$3" && labgrid-client -x ws://"$1":20408/ws places)

if [ -n "$places" ]
then
    list="List of acquired places: "
    list+=$places
    echo "$list"
fi
