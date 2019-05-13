var sensor = require('node-dht-sensor'); //little blue sensor modual
var fs = require('fs');
var path = require('path');
var terminator = require('./terminator');
var CronJob = require('cron').CronJob;

const WORKING_DIR = path.resolve('../secret-config');
const API_CONFIG = JSON.parse(fs.readFileSync(path.join(WORKING_DIR, 'api-config.json')));



var retries = 0;

function WX() { //fires every 15 minutes

    console.log('You will see this message every 15');
    sensor.read(11, 4, function(err, temperature, humidity) {
        if (!err) {
            var objToSend = {
                "location": API_CONFIG["LOCATION"],
                "temp": (temperature.toFixed(1)),
                "hum": (humidity.toFixed(1))
            }
            //console.log('Sending: ', objToSend);
            //calling the MQTT function
            terminator(objToSend);
            return;
        } else {
            console.log("there was an error", err);
            if (retries <= 2){
                retries++;
                WX(); //refire 
            } else {
                retries = 0;
                return;
            }
            
        }
    });

//}, null, true, 'America/New_York');

};
//setInterval(WX, 10000); //loops WX function every 10 seconds (10000 milliseconds) TO INFINITY AND BEYOND OR ATLEAST UNTIL A REBOOT
new CronJob('*/1 * * * * ', WX, null, true,'America/New_York');