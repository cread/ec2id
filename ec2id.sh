#!/bin/bash

cd /var/tmp
wget http://phrydde.net.s3.amazonaws.com/idapp.tar.bz2
tar fxj idapp.tar.bz2
cd idapp
./idapp.py >idapp.log &


