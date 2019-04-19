#!/bin/bash
PATH=/usr/local/bin:/usr/bin
cd /home/pi/apps/wx-client
git pull
echo "just did git pull"
npm install
echo "just ran npm install"
pm2 startOrRestart ecosystem.config.js
echo "just started or restarted ecosystem"
