#/bin/bash

sudo apt update
sudo apt install python-pip 
curl -fsSL https://get.docker.com -o get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
pip install conan conan_package_tools
 