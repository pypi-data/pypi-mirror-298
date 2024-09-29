# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

"""Labgrid methods for scotty-test."""

import subprocess
import logging
import shutil
import os


class Labgrid():
    """Labgrid methods implementation."""

    home_path = os.path.join(os.environ.get('HOME', '/does/not/exist'), 'scotty-labgrid')

    def create_client_directory(current_directory, machine):
        """Create a directory containing the client files."""
        src = f'{current_directory}/client'
        dest = os.path.join(Labgrid.home_path, 'client-{machine}')
        os.makedirs(Labgrid.home_path, exist_ok=True)
        shutil.copytree(src, dest)

    def start_coordinator(current_directory):
        """Start the coordinator Docker container."""
        output = ''
        cmd = 'docker ps | grep coordinator'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output += proc.communicate()[0].decode('utf-8')
        logging.getLogger(
                'scotty-test').info(f'{output}')
        if output == '':
            logging.getLogger(
                    'scotty-test').info('Starting Labgrid coordinator, please wait...')
            output = ''
            cmd = f'cd {current_directory}/labgrid && ./start-coordinator.sh'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output += proc.communicate()[0].decode('utf-8')
            logging.getLogger(
                    'scotty-test').info(f'{output}')

    def stop_coordinator(output):
        """Stop the coordinator Docker container."""
        output = output.split("\n")
        places = False
        for i in output:
            if "List of acquired places:" in i:
                places = True
        if places is False:
            logging.getLogger(
                'scotty-test').info('Stoping Labgrid coordinator, please wait...')
            output = ''
            cmd = 'docker stop coordinator'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output += proc.communicate()[0].decode('utf-8')
            logging.getLogger(
                    'scotty-test').info(f'{output}')

    def start_client(current_directory, machine):
        """Start the client Docker container."""
        if machine == "sm2s-intel-all":
            port_labgrid = 20408
            port_ssh = 2222
        if machine == "sm2s-imx8plus":
            port_labgrid = 20409
            port_ssh = 2223
        if machine == "sm2s-imx8nano":
            port_labgrid = 20410
            port_ssh = 2224
        output = ''
        cmd = f'cd {current_directory}/labgrid && ./start-client.sh {machine} {port_labgrid} {port_ssh}'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output += proc.communicate()[0].decode('utf-8')
        logging.getLogger(
                    'scotty-test').info(f'{output}')
        return output

    def set_client_run_tests_command(machine):
        """Add the start command in Dockerfile for the client running the tests."""
        client_dockerfile = f'{Labgrid.home_path}/client-{machine}/Dockerfile'
        with open(client_dockerfile, 'a') as file:
            file.write(f'CMD /home/labgrid-scripts/run-tests.sh root 172.17.0.2 {machine} /home/labgrid-venv/bin/activate')

    def set_client_release_place_command(machine):
        """Add the start command in Dockerfile for the client releasing the place."""
        client_dockerfile = f'{Labgrid.home_path}/client-{machine}/Dockerfile'
        with open(client_dockerfile, 'a') as file:
            file.write(f'CMD /home/labgrid-scripts/release-place.sh 172.17.0.2 {machine} /home/labgrid-venv/bin/activate')

    def set_client_image(machine, image):
        """Add the image to copy in the Dockerfile."""
        client_dockerfile = f'{Labgrid.home_path}/client-{machine}/Dockerfile'
        with open(client_dockerfile, 'a') as file:
            file.write(f'COPY {image}-{machine}.wic /tmp\n')

    def reset_client_dockerfile(machine):
        """Remove the client starting command and the image to copy in Dockerfile."""
        client_dockerfile = f'{Labgrid.home_path}/client-{machine}/Dockerfile'
        with open(client_dockerfile, "r+") as fp:
            lines = fp.readlines()
            fp.seek(0)
            for line in lines:
                if ('CMD' not in line) and ('COPY simplecore-simpleswitch-os' not in line):
                    fp.write(line)
            fp.truncate()

    def set_env_file(machine, image):
        """Add the right image to use in the environement file."""
        env_file = f'{Labgrid.home_path}/client-{machine}/env-{machine}.yaml'
        set_file = f'{Labgrid.home_path}/client-{machine}/set-env-{machine}.yaml'
        file = open(env_file, "r")
        data = open(set_file, "w")
        for x in file:
            if "sd_image" not in x:
                data.write(x)
            else:
                data.write(f"  sd_image: \"/tmp/{image}-{machine}.wic\"\n")
        file.close()
        data.close()
        os.remove(env_file)
        shutil.copy(set_file, env_file)
        os.remove(set_file)

    def get_ip_address(machine):
        """Return the IP address of the board."""
        ip_file = f'{Labgrid.home_path}/ip-{machine}.txt'
        with open(ip_file, "r") as file:
            ip = file.read()
        return ip

    def get_gpio_expander(machine):
        """Return the GPIO expander used by the board."""
        gpio_file = f'{Labgrid.home_path}/gpio-{machine}.txt'
        with open(gpio_file, "r") as file:
            gpio = file.read()
        return gpio

    def clean(machine, image):
        """Remove the client directory and the files containing the IP address and the GPIO expander."""
        ip_file = f'{Labgrid.home_path}/ip-{machine}.txt'
        os.remove(ip_file)
        gpio_file = f'{Labgrid.home_path}/gpio-{machine}.txt'
        os.remove(gpio_file)
        image_file = f'{Labgrid.home_path}/client-{machine}/{image}-{machine}.wic'
        os.remove(image_file)
        shutil.rmtree(f'{Labgrid.home_path}/client-{machine}')
