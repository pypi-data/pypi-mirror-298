# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
import re


def get_machine(shell):
    machine, _, status = shell.run('uname -n')
    assert status == 0
    machine = ''.join(machine)
    return machine


def get_ip_address(shell, interface):
    ip_string = shell.run_check("ip -o -4 addr show")

    regex = re.compile(
        r"""\d+:       # Match the leading number
        \s+(?P<if>\w+) # Match whitespace and interfacename
        \s+inet\s+(?P<ip>[\d.]+) # Match IP Adress
        /(?P<prefix>\d+) # Match prefix
        .*global # Match global scope, not host scope""", re.X
    )
    result = {}

    for line in ip_string:
        match = regex.match(line)
        if match:
            match = match.groupdict()
            result[match['if']] = match['ip']
    if result:
        return result[interface]

    return None


def test_get_ip(shell):
    ip = get_ip_address(shell, 'ETH0')
    assert ip is not None
    machine = get_machine(shell)
    ip_file = f'/home/labgrid-results/ip-{machine}.txt'
    with open(ip_file, "w") as f:
        f.write(ip)
