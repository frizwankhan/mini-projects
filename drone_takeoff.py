#!/usr/bin/env python


import rospy


from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from mavros_msgs.srv import SetMode

rospy.init_node('drone_takeoff')

                                             
def takeoff(height):
    mode_change = rospy.ServiceProxy('mavros/set_mode', SetMode)
    mode_change.call(custom_mode='GUIDED')

    for i in range(1000000):
        continue

    rospy.loginfo('mode change done')

    arming = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
    arming.call(True)

    for i in range(1000000):
        continue

    rospy.loginfo('arming done')

    taking_off = rospy.ServiceProxy('mavros/cmd/takeoff', CommandTOL)
    taking_off.call(altitude=height)

    rospy.spin()


takeoff(10)
