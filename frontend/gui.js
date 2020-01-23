var hasGP = false;
var repGP;

var connected = false;

// var client = new Paho.MQTT.Client(location.hostname, 1883, "clientId");
var client = null;

// var config = require('../config.json');
// var config = null;

// $.getJSON("../config.json", function(json) {
//     console.log(json); // this will show the info it in firebug console
//     config = json;
// });

// console.log(config);

function make_on_connect(topics) {
    let fn = function(reconnect, uri) {
        connected = true
        logEvent("MQTT CONNECTED!")

        for (let index = 0; index < topics.length; index++) {
            const topic = topics[index];
            
            client.subscribe(topic)
        }
    }

    return fn
}

function make_on_message() {
    let fn = function(msg) {
        logEvent("MQTT RECV: " + msg.payloadString)
    }

    return fn
}

function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        logEvent("onConnectionLost:"+responseObject.errorMessage);
        connected = false
    }
}

function connectMQTT() {
    let ip = $("#ipinput").val()
    logEvent("Connecting to [" + ip + "]...")
    client = new Paho.MQTT.Client(ip, 9001, "front_end");

    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = make_on_message();

    client.connect({onSuccess: make_on_connect(['li', 'ri'])});
}

function logEvent(str) {
    let $log = $("#log");
    console.log(str);
    $log.val($log.val() + "\n> " + str);

    $log.scrollTop($log[0].scrollHeight);
}

function txcallback(msg, topic) {
    if(client != null) {
        logEvent("DRIVE\t-> " + topic + ":" + String(msg))

        var sendMessage = new Paho.MQTT.Message(msg);
        sendMessage.destinationName = config["controller"]["topics"]["drive"][topic];

        // client.publish(config["controller"]["topics"]["drive"][topic], sendMessage);
        client.send(sendMessage);
    }
}

function rxcallback() {

}

var button_label = [
    "A",
    "B",
    "X",
    "Y",
    "LB",
    "RB",
    "LT",
    "RT",
    "back",
    "start",
    "xbox",
    "leftstick",
    "rightstick",
    "dpadleft",
    "dpadright",
    "dpadup",
    "dpaddown"
];

function createController(gamepad, callback) {
    var gp = {
        gp: gamepad,
        
        button_state: Array(gamepad.buttons.length).fill(false),
        
        ljx: 0.0,
        ljy: 0.0,
        rjx: 0.0,
        rjy: 0.0,

        callback: callback,
    };

    return gp
}

function refresh(gp) {
    for(var i = 0; i < gp.gp.buttons.length; i++) {
        if(gp.gp.buttons[i].pressed && !gp.button_state[i]) {
            gp.button_state[i] = true;
            gp.callback(String(2 * i), "button");

            logEvent(button_label[i] + " pressed!");
        } else if(!gp.gp.buttons[i].pressed && gp.button_state[i]) {
            gp.button_state[i] = false;
            gp.callback(String(2 * i + 1), "button");

            logEvent(button_label[i] + " released!");
        }
    }

    var ljx = gp.gp.axes[0];
    var ljy = gp.gp.axes[1];

    var rjx = gp.gp.axes[2];
    var rjy = gp.gp.axes[3];

    if(ljx != gp.ljx || ljy != gp.ljy) {
        gp.ljx = ljx;
        gp.ljy = ljy;

        logEvent("left joystick changed!");

        gp.callback(String(gp.ljx) + "," + String(gp.ljy), "left_joystick");
    } 

    if(rjx != gp.rjx || rjy != gp.rjy) {
        gp.rjx = rjx;
        gp.rjy = rjy;

        logEvent("right joystick changed!");

        gp.callback(String(gp.rjx) + "," + String(gp.rjy), "right_joystick");
    } 
}

var gamepads = {
    "drive": null
};

var gamepadList = [];


function canGame() {
    return "getGamepads" in navigator;
}

function refreshGamepads() {
    for(var i = 0; i < gamepadList.length; i++) {
        refresh(gamepadList[i]);
    }
}

$(document).ready(function() {

    if(canGame()) {
        $(window).on("gamepadconnected", function(e) {
            console.log(e)
            var gp = createController(navigator.getGamepads()[0], txcallback);
            gamepads.drive = gp;
            gamepadList.push(gp);
            logEvent("connection event for gamepad " + gp.gp.id);
            repGP = window.setInterval(refreshGamepads, 50);
        });

        $(window).on("gamepaddisconnected", function(e) {
            console.log(e)
            logEvent("disconnection event for gamepad" + e.gamepad.id);
            window.clearInterval(repGP);
        });
    }

});