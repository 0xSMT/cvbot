var config = {
    "mqtt" : {
        "topics": ["q", "w", "e", "y", "p", "l"],
        "server": "localhost"
    },
    "ros": {
        "arduino": "a",
        "img_from_lefteye_topic": "limg",
        "img_from_righteye_topic": "rimg",
        "left_img_from_master_topic": "li",
        "right_img_from_master_topic": "ri"
    },
    "controller": {
        "map": {
            "a_press": 0,
            "a_release": 1,
            "b_press": 2,
            "b_release": 3,
            "x_press": 4,
            "x_release": 5,
            "y_press": 6,
            "y_release": 7,
            "l_bumper_press": 8,
            "l_bumper_release": 9,
            "r_bumper_press": 10,
            "r_bumper_release": 11,
            "left_trigger_press": 12,
            "left_trigger_release": 13,
            "right_trigger_press": 14,
            "right_trigger_release": 15,
            "dpad_up_press": 30,
            "dpad_up_release": 31,
            "dpad_right_press": 28,
            "dpad_right_release": 29,
            "dpad_down_press": 32,
            "dpad_down_release": 33,
            "dpad_left_press": 26,
            "dpad_left_release": 27,
            "start_press": 18,
            "start_release": 19,
            "back_press": 16,
            "back_release": 17,
            "left_joystick_move": "ljm",
            "right_joystick_move": "rjm"
        },
        "names": [
            "drive"
        ],
        "topics": {
            "drive": {
                "button": "q",
                "left_joystick": "w",
                "right_joystick": "e",
                "right_trigger": "r",
                "left_trigger": "t"
            }
        }
    }
}