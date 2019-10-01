var hasGP = false;
var repGP;

function logEvent(str) {
    let $log = $("#log");
    console.log(str);
    $log.val($log.val() + "\n> " + str);
}

function txcallback(value, topic) {

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
    for(var i = 0;i < gp.gp.buttons.length; i++) {
        if(gp.gp.buttons[i].pressed && !gp.button_state[i]) {
            gp.button_state[i] = true;
            gp.callback(2 * i, "button");

            logEvent(button_label[i] + " pressed!");
        } else if(!gp.gp.buttons[i].pressed && gp.button_state[i]) {
            gp.button_state[i] = false;
            gp.callback(2 * i + 1, "button");

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
    "drive": null,
    "mine": null
};

var gamepadList = [];

// function assignGamepads() {
//     for(var key in gamepads) {
//         if (!gamepads.hasOwnProperty(key)) continue;

//         // do an alert for pressing a button on a controller for the associated controller (press A for 'key')
//         logEvent("Press 'A' on the " + key + " controller!");
//     }
// }

function canGame() {
    return "getGamepads" in navigator;
}

function refreshGamepads() {
    for(var i = 0; i < gamepadList.length; i++) {
        refresh(gamepadList[i]);
    }

    // var gp = navigator.getGamepads()[0];
    // var html = "";
    //     html += "id: "+gp.id+"<br/>";

    // for(var i=0;i<gp.buttons.length;i++) {
    //     html+= "Button "+(i+1)+": ";
    //     if(gp.buttons[i].pressed) html+= " pressed";
    //     html+= "<br/>";
    // }

    // for(var i=0;i<gp.axes.length; i+=2) {
    //     html+= "Stick "+(Math.ceil(i/2)+1)+": "+gp.axes[i]+","+gp.axes[i+1]+"<br/>";
    // }

    // $("#gamepadDisplay").html(html);
}

$(document).ready(function() {

    if(canGame()) {
        // var prompt = "To begin using your gamepad, connect it and press any button!";
        // $("#gamepadPrompt").text(prompt);

        $(window).on("gamepadconnected", function(e) {
            console.log(e)
            // var gp = navigator.getGamepads()[e.gamepad.index];
            var gp = createController(navigator.getGamepads()[0], txcallback);

            gamepadList.push(gp);
            logEvent("connection event for gamepad " + gp.gp.id);
            repGP = window.setInterval(refreshGamepads, 50);
        });

        $(window).on("gamepaddisconnected", function(e) {
            console.log(e)
            logEvent("disconnection event for gamepad" + e.gamepad.id);
            // $("#gamepadPrompt").text(prompt);
            window.clearInterval(repGP);
        });

        //setup an interval for Chrome
        // var checkGP = window.setInterval(function() {
        //     // console.log('checkGP');
        //     if(navigator.getGamepads()[0]) {
        //         if(!hasGP) $(window).trigger("gamepadconnected");
        //         window.clearInterval(checkGP);
        //     }
        // }, 500);
    }

});