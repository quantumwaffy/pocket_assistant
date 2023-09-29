#! /bin/bash

#Update packages
sudo apt update -y

#Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install -y docker-ce
sudo usermod -aG docker ${default_user}

#Make
sudo apt install -y make

#Git
sudo apt install -y make git
