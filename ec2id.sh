#!/bin/bash

cd /var/tmp
wget -O ec2id.tar.gz http://github.com/cread/ec2id/tarball/master
tar fxz ec2id.tar.gz
cd cread-ec2id-*

echo -n "Starting up ec2id in $(pwd)..."

nohup python ec2id.py > ec2id.log &

echo "done!"

