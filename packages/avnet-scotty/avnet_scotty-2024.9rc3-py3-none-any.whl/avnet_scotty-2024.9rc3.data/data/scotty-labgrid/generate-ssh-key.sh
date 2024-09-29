#!/bin/bash
# SPDX-FileCopyrightText: (C) 2024 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

# Script to generate ssh key
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
echo 'PermitRootLogin without-password' >> /etc/ssh/sshd_config
service ssh restart
ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa
hostname=$(env | grep HOSTNAME) 
hostname=${hostname//HOSTNAME=/}
/home/labgrid-scripts/interactive-ssh-copy-id.sh "$hostname" "$1"
