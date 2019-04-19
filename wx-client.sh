#!/bin/bash
cd /home/pi/apps/wx-client
echo pwd
git pull
echo "just did git pull"
npm install
echo "just ran npm install"
pm2 startOrRestart ecosystem.config.js
echo pm2 ls