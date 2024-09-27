# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

def get_machine(shell):
    machine, _, status = shell.run('uname -n')
    assert status == 0
    machine = ''.join(machine)
    return machine


def get_gpio_expander_device(target):
    resources = target.resources
    for i in resources:
        resource_name = i.name
        if "gpio_expander" in resource_name:
            gpio_expander_name = resource_name
    gpio_expander = target.get_resource('NetworkSerialPort', name=gpio_expander_name, wait_avail=False)
    device = gpio_expander.extra["path"]
    return device


def test_gpio_expander(target, shell):
    machine = get_machine(shell)
    device = get_gpio_expander_device(target)
    assert device is not None
    gpio_file = f'/home/labgrid-results/gpio-{machine}.txt'
    with open(gpio_file, "w") as f:
        f.write(device)
