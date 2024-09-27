#!/usr/bin/expect
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# shellcheck disable=SC1071

set HOSTNAME [lindex $argv 0]
set PASSWORD [lindex $argv 1]
spawn ssh-copy-id root@$HOSTNAME
expect "Are you sure you want to continue connecting (yes/no)?"
send "yes\r"
expect "root@$HOSTNAME's password:"
send "$PASSWORD\r"
interact
