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

if ! dotnet --version &> /dev/null; then
    echo ".NET is not installed. Installing .NET..."

    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
    sudo dpkg -i packages-microsoft-prod.deb
    rm packages-microsoft-prod.deb

    sudo apt-get update; \
    sudo apt-get install -y apt-transport-https && \
    sudo apt-get update && \
    sudo apt-get install -y dotnet-sdk-6.0

    echo ".NET installed successfully."
else
    echo ".NET is already installed."
fi
