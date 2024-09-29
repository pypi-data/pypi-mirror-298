# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

"""Configuration for the Labgrid tests."""
import pytest


# Fixtures for the consoles
@pytest.fixture
def shell(strategy):
    """Return the shell of the board."""
    strategy.transition('shell', strategy.overlays)
    return strategy.shell


@pytest.fixture
def gpioexpander(target):
    """Return the GPIO Expander of the board."""
    gpioexpander = target.get_driver('GPIOExpanderDriver')
    return gpioexpander
