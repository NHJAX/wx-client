#!/bin/bash
cd /home/pi/apps/wx-client
git pull
npm install
pm2 startOrRestart ecosystem.config.js