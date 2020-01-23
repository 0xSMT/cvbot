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
        
        ljx = 0.0,
        ljy = 0.0,
        rjx = 0.0,
        rjy = 0.0,

        callback: callback,

        refresh: function() {
            for(var i = 0;i < this.gp.buttons.length; i++) {
                if(this.gp.buttons[i].pressed && !this.button_state[i]) {
                    this.button_state[i] = true;
                    this.callback([2 * i], "button");
                } else if(!this.gp.buttons[i].pressed && this.button_state[i]) {
                    this.button_state[i] = false;
                    this.callback([2 * i + 1], "button");
                }
            }

            var ljx = this.gp.axes[0];
            var ljy = this.gp.axes[1];

            var rjx = this.gp.axes[0];
            var rjy = this.gp.axes[1];

            if(ljx != this.ljx || ljy != this.ljy) {
                this.ljx = ljx;
                this.ljy = ljy;

                this.callback(String(this.ljx) + "," + String(this.ljy), "left_joystick");
            } 

            if(rjx != this.rjx || rjy != this.rjy) {
                this.rjx = rjx;
                this.rjy = rjy;

                this.callback(String(this.rjx) + "," + String(this.rjy), "right_joystick");
            } 
        }
    };

    return gp
}