#!/usr/bin/env bash
git pull origin master
python setup.py install
sudo pkill -f -9 supervisor
sudo pkill -f -9 python
sudo -E supervisord -c /root/jobwork.io/jobwork/conf/supervisord.conf
