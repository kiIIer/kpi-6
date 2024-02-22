#!/bin/bash

SSHD_CONFIG="/etc/ssh/sshd_config"

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

sed -i.bak 's/^#Port 22/Port 23/' "$SSHD_CONFIG"

if grep -q "^Port 23" "$SSHD_CONFIG"; then
  echo "Port changed to 23 successfully."
  systemctl restart sshd
else
  echo "Failed to change the port. Please check the sshd_config file."
fi

sudo apt-get update

sudo apt-get install -y python3 python3-pip

pip3 install Flask

nohup python3 sync/server.py &