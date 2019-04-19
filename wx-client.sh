#!/bin/bash
git pull
npm install
pm2 startOrRestart ecosystem.config.js