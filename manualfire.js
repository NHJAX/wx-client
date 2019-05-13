var sensor = require('node-dht-sensor'); //little blue sensor modual
var fs = require('fs');
var path = require('path');

//function WX() {

    sensor.read(11, 4, function(err, temperature, humidity) {
        if (!err) {
            var objToSend = {
                "location": API_CONFIG["LOCATION"],
                "temp": (temperature.toFixed(1)),
                "hum": (humidity.toFixed(1))
            }
            //console.log('Sending: ', objToSend);
            //calling the MQTT function
            console.log(objToSend);
        } else {
            console.log("there was an error", err);
            WX();
        }
    });

}, null, true, 'America/New_York');

//}
//setInterval(WX, 10000); //loops WX function every 10 seconds (10000 milliseconds) TO INFINITY AND BEYOND OR ATLEAST UNTIL A REBOOT
