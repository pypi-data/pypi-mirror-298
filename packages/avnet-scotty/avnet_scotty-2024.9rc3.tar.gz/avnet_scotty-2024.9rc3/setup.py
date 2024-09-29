# SPDX-FileCopyrightText: (C) 2022 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# noqa: D100

import setuptools
import os

_version = os.environ.get('SCOTTY_VERSION', '0.0.1')

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description = '''
Scotty is a tool to make the process of building the SimpleCore™ Distro distribution
reproducible on any Linux and Windows computer (compatible with WSL2). It uses a
container to setup the same environment used by our continuous integration
process to ensure that the build on your machine will always be successful for
any of our standard images. Scotty is based on standard open-source tools such as
Docker, repo, ... and mimics the standard bitbake command set (standard tool for
Yocto builds). If you are not familiar with building Yocto BSPs, we strongly
recommend that you use Scotty to start with.

For more details please visit our [Documentation](https://simple.embedded.avnet.com/index.hmtl?link=tools/scotty/README.html).
'''

setuptools.setup(
    author='Avnet Embedded GmbH',
    description='scotty: S(imple)C(ore) O(pen) T(echnology) T(ool for) Y(ou)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL-3.0-only',
    license_files=('LICENSE',),
    entry_points={
        'console_scripts': [
            'bumper = bumper.__main__:main',
            'scotty-test = scotty_test.__main__:main',
        ],
    },
    project_urls={
        'Documentation': 'https://simple.embedded.avnet.com/?link=tools/scotty/README.html',
        'SimpleCore Documentation': 'https://simple.embedded.avnet.com/',
        'Source Code': 'https://github.com/avnet-embedded/simplecore-tools/tree/kirkstone/scotty'
    },
    data_files=[('scotty-labgrid',
                 [
                     'scotty-labgrid/start-coordinator.sh',
                     'scotty-labgrid/start-client.sh',
                     'scotty-labgrid/coordinator/Dockerfile',
                     'scotty-labgrid/coordinator/coordinator.sh',
                     'scotty-labgrid/client/gpioexpanderdriver.py',
                     'scotty-labgrid/client/exporter-sm2s-intel-all.yaml',
                     'scotty-labgrid/client/generate-ssh-key.sh',
                     'scotty-labgrid/client/simpleswitchstrategy.py',
                     'scotty-labgrid/client/interactive-ssh-copy-id.sh',
                     'scotty-labgrid/client/exporter-sm2s-imx8nano.yaml',
                     'scotty-labgrid/client/release-place.sh',
                     'scotty-labgrid/client/env-sm2s-imx8plus.yaml',
                     'scotty-labgrid/client/env-sm2s-imx8nano.yaml',
                     'scotty-labgrid/client/testsuite/test_ip.py',
                     'scotty-labgrid/client/testsuite/test_gpio_expander.py',
                     'scotty-labgrid/client/testsuite/conftest.py',
                     'scotty-labgrid/client/Dockerfile',
                     'scotty-labgrid/client/env-sm2s-intel-all.yaml',
                     'scotty-labgrid/client/run-tests.sh',
                     'scotty-labgrid/client/exporter-sm2s-imx8plus.yaml',
                 ])],
    packages=[
        'bumper',
        'scotty_test',
        'scotty_test.labgrid',
        'scotty_test.menu',
        'scotty_test.reporter',
        'scotty_test.runner',
        'scotty_test.storage',
        'scotty_test.utils',
    ],
    install_requires=requirements,
    include_package_data=True,
    # As scotty is already in use on PyPi our package is called
    # avnet-scotty
    name='avnet-scotty',
    scripts=[
        'scotty',
        'scotty-runqemu',
        'scripts/vm_bundle.sh',
        'scripts/vm_create.sh.template',
    ],
    version=_version,
)
