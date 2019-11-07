#!/usr/bin/env python

"""A class for representing the robot state in terms of continuous values.
Samuel Taylor

RobotState contains various values for representing the output state of the robot. In other words,
this class acts as an abstraction of the robot's physical output signals. Rather than storing the
signals sent to controllers, the RobotState class contains a theoretical representation of the robot,
such as (auger at 50% power, wheels at 75% forward, everything else at 0%), leaving the interpretation
of these values to the Arduino or whichever chip is connected to the motor control hardware.
"""

import drive_controller_fns
# import mine_controller_fns

# Helper method to import functions by their literal name. Used to obtain references to the callback
# functions in the `drive_controller_fns.py` and `mine_controller_fns.py` files. 
def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

class RobotState:
    """Defaults the robot state to all 0s"""
    def __init__(self):
        self.front_left  = 0.0
        self.front_right = 0.0
        self.rear_left   = 0.0
        self.rear_right  = 0.0

        # A flag for autonomous. Currently unused.
        self.auto = False

        # A flag for denoting whether robot state has been changed.
        self.stale = False
    
    # Returns the robot state as a vector of real-valued numbers. Note that the order matters, and the chip that receives this transmission
    # must take order into account.
    # TODO: Instead, send a tuple with a motor (or motor-set) ID and a new motor value. Will lighten the data transmission bottleneck
    # That occurs with larger vector sizes.
    def as_arr(self):
        return [self.front_left, self.front_right, self.rear_left, self.rear_right]

"""" A dummy function for empty behavior. """
def do_nothing(rs):
    ()

"""A function for stopping all motors. (unused)"""
def stop_all(rs):
    rs.front_left  = 0.0
    rs.front_right = 0.0
    rs.rear_left   = 0.0
    rs.rear_right  = 0.0

"""Builds a dictionary of controllers and their input callbacks. The dictionary has the following layout:

    map[controller_name][signal_from_controller] = corresponding_controller_callback_for_signal()

For example, the callback for a B button release on the mining controller might be accessed as follows:

    map["mine"][3]()

Assuming we are going by the information stored in `mqtt_config.json`. Through this system, any number of
controllers can be used with any number of associated inputs.
The `names` argument is the list of controller names that should be used.
The `json_con` argument contains a json dictionary (see the controller:map dictionary in the `mqtt_config.json` file
for an example) of the input name and the corresponding signal received over the MQTT channel. 
"""
def make_controller_map(json_con, names):
    controller_map = {}

    # For each of the controller names...
    for name in names:
        # Construct a new dictionary for that controller...
        controller_map[name] = {}
        # ...and for each input in the controller map...
        for key in json_con:
            # ...set a reference to the approproate callback, importing the function by name according the the associated key
            # in the JSON file.
            controller_map[name][json_con[key]] = import_from(name + "_controller_fns", "on_" + key)
    
    return controller_map
