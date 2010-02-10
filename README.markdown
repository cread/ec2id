ec2id
=====

*ec2id* is a simple web application to display instance metadata from a running EC2 instance. 

For more information on AWS Instance Metadata read the [documentation](http://docs.amazonwebservices.com/AWSEC2/latest/DeveloperGuide/index.html?AESDG-chapter-instancedata.html)

Deploying from User Data
------------------------

EC2 allows you to specify upto 16Kb of user data when launching an instance. The better classes of AMI (such as those provided by [Alestic](http://alestic.com/)) will execute that user data as a script if it starts with `#!`. This allows you to launch *ec2id* when your instance starts.

Here's a sample script you could use:

    #!/bin/bash
    cd /var/tmp
    wget http://ec2id.s3.amazonaws.com/ec2id.tar.bz2
    tar fxj ec2id.tar.bz2
    cd ec2id
    python ec2id.py >/dev/null &





