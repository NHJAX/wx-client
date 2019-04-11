var sensor = require('node-dht-sensor'); //little blue sensor modual
var fs = require('fs');
var path = require('path');

const WORKING_DIR = path.resolve('../secret-config');
const API_CONFIG = JSON.parse(fs.readFileSync(path.join(WORKING_DIR, 'api-config.json')));

var terminator = require('./terminator');

sensor.read(11, 4, function(err, temperature, humidity) {
    if (!err) {
        var objToSend = {
            "location": API_CONFIG["location"],
            "temp": (temperature.toFixed(1)),
            "hum": (humidity.toFixed(1))
        }
        console.log('Sending: ', objToSend);
        //calling the MQTT function
        terminator("T", objToSend);
    } else {
        console.log("there was an error", err);
    }

});