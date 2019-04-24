var temp; //global variable for DHT Sensors
var hum; //global variable for DHT Sensors
var mqtt = require('mqtt'); //import modual
var fs = require('fs') //File System imported
var path = require('path') //Path imported

const WORKING_DIR = path.resolve('../secret-config');
var SECURE_KEY = path.join(WORKING_DIR, 'certs' + '/wxKey.pem'); //Location of secure key - path to key only, DO NOT READ THE KEY
var SECURE_CERT = path.join(WORKING_DIR, 'certs' + '/wxCert.pem'); //Location of Secure Cert - path to key only, DO NOT READ THE CERT
const API_CONFIG = JSON.parse(fs.readFileSync(path.join(WORKING_DIR, 'api-config.json')));


var SECURE_KEY_BUF = Buffer.from(fs.readFileSync(path.join(WORKING_DIR, 'certs', 'wxKey.pem'))); //__dirname + '/tls-key.pem'; //Location of secure key
var SECURE_CERT_BUF = Buffer.from(fs.readFileSync(path.join(WORKING_DIR, 'certs', 'wxCert.pem')));

var PORT = API_CONFIG["SECURE_PORT"]; //MQTT secure port
var HOST = API_CONFIG["WX_SERVER"]; ////Machine that has "SKYNET"

console.log('████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗      ██████╗     ███╗   ██╗    ██╗         ██╗    ███╗   ██╗    ███████╗')
console.log('╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗    ██╔═══██╗    ████╗  ██║    ██║         ██║    ████╗  ██║    ██╔════╝')
console.log('   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║   ██║██████╔╝    ██║   ██║    ██╔██╗ ██║    ██║         ██║    ██╔██╗ ██║    █████╗  ')
console.log('   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║   ██║██╔══██╗    ██║   ██║    ██║╚██╗██║    ██║         ██║    ██║╚██╗██║    ██╔══╝  ')
console.log('   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ╚██████╔╝██║  ██║    ╚██████╔╝    ██║ ╚████║    ███████╗    ██║    ██║ ╚████║    ███████╗')
console.log('   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝     ╚═════╝     ╚═╝  ╚═══╝    ╚══════╝    ╚═╝    ╚═╝  ╚═══╝    ╚══════╝')


var callMQTT = function(data) { //wrapped MQTT message handler in function callMQTT
    console.log('inside callMQTT', data);

    var options = { //Options sets up MQTT connection
        port: PORT,
        host: HOST,
        key: SECURE_KEY_BUF.toString(),
        cert: SECURE_CERT_BUF.toString(),
        rejectUnauthorized: false,
        protocol: 'mqtts'
    };
    //console.log(options);

    var client = mqtt.connect(options);

    let obj = {}; //oject is assigned value
    //console.log('data', data);

    obj.MQTT_TOPIC = "waitTimes";
    obj.location = API_CONFIG["LOCATION"];
    obj.msg = {"Greeting":"hi"};
    console.log(obj);

    client.on('connect', function() { //MQTT message handler "Publisher"
        //console.log('connect');
        var MQTT_TOPIC = obj.MQTT_TOPIC;
        client.subscribe(MQTT_TOPIC, function(err) {
            console.log('subscribe');
            if (!err) {
                buf = Buffer.from(JSON.stringify(obj)); //buffer is dumped into a JSON object using obj
                client.publish(MQTT_TOPIC, buf); //message is pulished to subscriber
                console.log("Message sent successfully" + buf, Date.now());
                client.end()
            }
            else {
              console.log('err', err);
            }
        })
    });

    client.on('error', function() { //Error handler
        console.log("\nDANGER WILL ROBINSON ERROR ERROR MESSAGE HANDLER FAILED DESTROY ROBINSON FAMILY DESTROY JUPITER ONE\n");
        client.end()
    });

};

callMQTT({"foo":"bar"});

//module.exports = callMQTT;

//setInterval(WX, 10000); //loops WX function every 10 seconds (10000 milliseconds) TO INFINITY AND BEYOND OR ATLEAST UNTIL A REBOOT
