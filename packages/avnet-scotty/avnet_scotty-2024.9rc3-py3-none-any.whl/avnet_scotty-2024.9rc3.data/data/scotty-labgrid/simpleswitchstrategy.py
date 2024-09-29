# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

"""Simpleswitch strategy driver."""

import enum
import attr
from labgrid.factory import target_factory
from labgrid.step import step
from labgrid.strategy import Strategy, StrategyError


class Status(enum.Enum):
    """Give the status of the board."""

    unknown = 0
    off = 1
    shell = 2


@target_factory.reg_driver
@attr.s(eq=False)
class SimpleSwitchStrategy(Strategy):
    """Imx8plusStrategy - Strategy to switch to shell."""

    bindings = {
        "power": "PowerProtocol",
        "sdmux": "USBSDWireDriver",
        "storage": "USBStorageDriver",
        "console": "ConsoleProtocol",
        "shell": "ShellDriver",
    }

    status = attr.ib(default=Status.unknown)
    overlays = attr.ib(default="")

    def __attrs_post_init__(self):
        """Set the attributes after initialization."""
        super().__attrs_post_init__()
        self.bootstrapped = False
        self.bool_set_overlays = False

    @step()
    def bootstrap(self):
        """Flash the SD Card using the SDWireC."""
        self.target.activate(self.sdmux)
        self.sdmux.set_mode("host")
        self.target.activate(self.storage)
        image = self.target.env.config.get_image_path("sd_image")
        self.storage.write_image(image)
        self.target.deactivate(self.storage)
        self.sdmux.set_mode("dut")
        self.bootstrapped = True

    @step(args=['status'])
    def transition(self, status, overlays, *, step):  # pylint: disable=redefined-outer-name
        """Do the transitions to the different statuses."""
        if not isinstance(status, Status):
            status = Status[status]
        if status == Status.unknown:
            raise StrategyError(f"can not transition to {status}")
        elif status == self.status:
            step.skip("nothing to do")
            return  # nothing to do
        elif status == Status.off:
            self.target.deactivate(self.console)
            self.target.activate(self.power)
            self.power.off()
        elif status == Status.shell:
            self.transition(Status.off, overlays)
            if not self.bootstrapped:
                self.bootstrap()
            self.target.activate(self.console)
            self.power.cycle()
            self.target.activate(self.shell)
            self.shell.run("systemctl is-system-running --wait")
        else:
            raise StrategyError(
                f"no transition found from {self.status} to {status}"
            )
        self.status = status

    @step(args=['status'])
    def force(self, status, *, step):  # pylint: disable=redefined-outer-name
        """Force the transition to the statuses."""
        if not isinstance(status, Status):
            status = Status[status]
        if status == Status.unknown:
            raise StrategyError(f"can not force state {status}")
        elif status == Status.off:
            self.target.deactivate(self.shell)
            self.target.activate(self.power)
        elif status == Status.shell:
            self.target.activate(self.power)
            self.target.activate(self.shell)
        else:
            raise StrategyError(f"not setup found for {status}")
        self.status = status
