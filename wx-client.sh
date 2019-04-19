#!/bin/bash
cd /home/pi/apps/wx-client
git pull
echo "just did git pull"
/usr/local/bin/npm install
echo "just ran npm install"
/usr/local/bin/pm2 startOrRestart ecosystem.config.js
echo "just started or restarted ecosystem"
