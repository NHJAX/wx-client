var sensor = require('node-dht-sensor'); //little blue sensor modual

var retries = 0;
var tempright = 0;
var templeft = 0;
var humright = 0;
var humleft = 0;
var objToSendright = "";
var objToSendleft = "";

function WX(tempright, templeft, humleft, humright) { //fires every 15 minutes

    sensor.read(11, 4, function(err, tempright, humright) {
        if (!err) {
            var objToSendright = {
                "temp": (tempright.toFixed(1)),
                "hum": (humright.toFixed(1))
            }
            console.log('Sending: ', objToSendright);
            //calling the MQTT function
            //terminator(objToSend);
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

    sensor.read(11, 17, function(err, templeft, humleft) {
        if (!err) {
            let humleft = humleft;
            var objToSendleft = {
                "temp": (templeft.toFixed(1)),
                "hum": (humleft.toFixed(1))
            }
            console.log('Sending: ', objToSendleft);
            //calling the MQTT function
            //terminator(objToSend);
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
    function CL(humleft, humright) {
      console.log(humleft);
      console.log(humright);
    };
    setTimeout(CL, 3000);

//}, null, true, 'America/New_York');

};
WX();
//setInterval(WX, 10000); //loops WX function every 10 seconds (10000 milliseconds) TO INFINITY AND BEYOND OR ATLEAST UNTIL A REBOOT
