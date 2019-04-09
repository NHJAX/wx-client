var mqtt = require('mqtt') //MQTT imported
var fs = require('fs') //File System imported
var path = require('path') //Path imported
var KEY = fs.readFileSync(path.join(__dirname, '/tls-key.pem')) //Secure Key location
var CERT = fs.readFileSync(path.join(__dirname, '/tls-cert.pem')) //Secure Cert location
var MQTT_TOPIC          = "jax"; //MQTT Topic is set
var PORT = 8883 //MQTT secure port
var HOST = 'localhost' //Machine that has server "SKYNET"

console.log('████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗      ██████╗     ███╗   ██╗    ██╗         ██╗    ███╗   ██╗    ███████╗')
console.log('╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗    ██╔═══██╗    ████╗  ██║    ██║         ██║    ████╗  ██║    ██╔════╝')
console.log('   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║   ██║██████╔╝    ██║   ██║    ██╔██╗ ██║    ██║         ██║    ██╔██╗ ██║    █████╗  ')
console.log('   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║   ██║██╔══██╗    ██║   ██║    ██║╚██╗██║    ██║         ██║    ██║╚██╗██║    ██╔══╝  ')
console.log('   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ╚██████╔╝██║  ██║    ╚██████╔╝    ██║ ╚████║    ███████╗    ██║    ██║ ╚████║    ███████╗')
console.log('   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝     ╚═════╝     ╚═╝  ╚═══╝    ╚══════╝    ╚═╝    ╚═╝  ╚═══╝    ╚══════╝')

var options = { //Options sets up MQTT connection
  port: PORT,
  host: HOST,
  key: KEY,
  cert: CERT,
  rejectUnauthorized: false,
  protocol: 'mqtts'
}

var client = mqtt.connect(options) //MQTT connection is built

client.on('connect', function () { //MQTT message handler "Publisher"
  client.subscribe(MQTT_TOPIC, function (err) { //Client "Terminator" looks for someone to talk to
    if (!err) {
      let msg = ("Hi Skynet this is T-800") //Message is developed
      let buf = ("Topic = " + MQTT_TOPIC + " Message = " + msg) //Message is developed
      client.publish(MQTT_TOPIC, buf); //message is pulished to subscriber
      console.log("Message sent successfully " + buf); //local success message printed
    }
  })
})
