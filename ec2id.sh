#!/bin/bash

cd /var/tmp
wget http://ec2id.s3.amazonaws.com/ec2id.tar.bz2
tar fxj ec2id.tar.bz2
cd ec2id
./ec2id.py >ec2id.log &


