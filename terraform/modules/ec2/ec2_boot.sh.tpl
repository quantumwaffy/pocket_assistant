#! /bin/bash

#Update packages
sudo yum update -y

#Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

#Make
sudo yum -y install make

#Git
sudo yum -y install git
