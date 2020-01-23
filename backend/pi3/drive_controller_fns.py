import rospy

def on_a_press(rs):
    # rs.auto = not rs.auto
    rospy.loginfo("drive a pressed")
    
    # rs.auger_out = 1.0
    # rs.stale = True

def on_a_release(rs):
    rospy.loginfo("drive a released")
    
    # rs.auger_out = 0.0
    # rs.stale = True

def on_b_press(rs):
    rospy.loginfo("drive b pressed")
    
    # rs.auger_out = -1.0
    # rs.stale = True

def on_b_release(rs):
    rospy.loginfo("drive b released")

    # rs.auger_out = 0.0
    # rs.stale = True

def on_x_press(rs):
    rospy.loginfo("drive x pressed")

    # rs.auger_tilt = 1.0
    # rs.stale = True

def on_x_release(rs):
    rospy.loginfo("drive x released")

    # rs.auger_tilt = 0.0
    # rs.stale = True

def on_y_press(rs):
    rospy.loginfo("drive y pressed")

    # rs.auger_tilt = -1.0
    # rs.stale = True

def on_y_release(rs):
    rospy.loginfo("drive y released")

    # rs.auger_tilt = 0.0
    # rs.stale = True

def on_l_bumper_press(rs):
    rospy.loginfo("drive left bumper pressed")

    # rs.dumper = 1.0
    # rs.stale = True

def on_l_bumper_release(rs):
    rospy.loginfo("drive left bumper released")

    # rs.camera_up = 0.0
    # rs.stale = True

    # rs.dumper = 0.0
    # rs.stale = True

def on_r_bumper_press(rs):
    rospy.loginfo("drive right bumper pressed")

    # rs.dumper = -1.0
    # rs.stale = True

def on_r_bumper_release(rs):
    rospy.loginfo("drive right bumper released")

    # rs.dumper = 0.0
    # rs.stale = True

def on_left_joystick_move(rs, x, y):
    rospy.loginfo("drive ljs moved")
    rs.front_left = -y
    rs.rear_left = -y

    rs.stale = True

def on_right_joystick_move(rs, x, y):
    rospy.loginfo("drive rjs moved")
    rs.front_right = y
    rs.rear_right = y

    rs.stale = True

def on_right_trigger_release(rs, val):
    rospy.loginfo("drive rt release")

def on_right_trigger_press(rs, val):
    rospy.loginfo("drive rt press")

def on_left_trigger_release(rs, val):
    rospy.loginfo("drive lt release")

def on_left_trigger_press(rs, val):
    rospy.loginfo("drive lt press")

def on_dpad_up_press(rs):
    rospy.loginfo("drive dpad up pressed")


def on_dpad_up_release(rs):
    rospy.loginfo("drive dpad up released")
    
    # rs.camera_up = 0.0
    # rs.stale = True

def on_dpad_left_press(rs):
    rospy.loginfo("drive dpad left pressed")


def on_dpad_left_release(rs):
    rospy.loginfo("drive dpad left released")

def on_dpad_down_press(rs):
    rospy.loginfo("drive dpad down pressed")


def on_dpad_down_release(rs):
    rospy.loginfo("drive dpad down released")
        
    # rs.camera_up = 0.0
    # rs.stale = True

def on_dpad_right_press(rs):
    rospy.loginfo("drive dpad right pressed")


def on_dpad_right_release(rs):
    rospy.loginfo("drive dpad right released")

def on_start_press(rs):
    rospy.loginfo("drive start pressed")

def on_start_release(rs):
    rospy.loginfo("drive start released")

def on_back_press(rs):
    rospy.loginfo("drive back pressed")

def on_back_release(rs):
    rospy.loginfo("drive back released")
