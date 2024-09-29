# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

"""Driver for the GPIO Expander."""
import attr
from labgrid.factory import target_factory
from labgrid.driver import Driver
from labgrid.driver.consoleexpectmixin import ConsoleExpectMixin
from labgrid.protocol import ConsoleProtocol


@target_factory.reg_driver
@attr.s(eq=False)
class GPIOExpanderDriver(ConsoleExpectMixin, Driver, ConsoleProtocol):
    """GPIO Expander Driver class."""

    bindings = {"port": {"SerialPort", "NetworkSerialPort"}, }

    def __attrs_post_init__(self):
        """Set up the attributes of the GPIO Expander Driver."""
        super().__attrs_post_init__()
