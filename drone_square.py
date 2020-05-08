#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
import math

# variable to store the value of current pose of drone
pose = PoseStamped()
# variable to store value of set_point
msg = PoseStamped()

# call back function store the value of current pose of the drone


def callback(pose_message):
    global pose
    pose = pose_message

# publisher function publishes the pose into the setpoint_postition topic


def publisher(p, q, r):
    global msg
    msg.pose.position.x = p
    msg.pose.position.y = q
    msg.pose.position.z = r
    pub.publish(msg)
    rospy.loginfo('published')

# to check if the drone has reached a particular setpoint


def checking_goal_point(p, q):
    global pose
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
        if getdistance(pose.pose.position.x,  pose.pose.position.y, p, q):
            break
        else:
            continue


def getdistance(x1, y1, x2, y2):
    if math.sqrt(((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2))) < 1:
        rospy.loginfo('equals')
        return 1
    else:
        rospy.loginfo('not equal')
        return 0


if __name__ == "__main__":
    try:
        rospy.init_node('publisher', anonymous=True)
        pub = rospy.Publisher(
            '/mavros/setpoint_position/local', PoseStamped, queue_size=10)
        rospy.Subscriber('/mavros/local_position/pose', PoseStamped, callback)

        for k in range(200):
            continue
        rospy.loginfo('publishing 5,0')
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rate.sleep()
            publisher(5, 0, 10)
            if getdistance(pose.pose.position.x,  pose.pose.position.y, 5, 0):
                break
            else:
                continue

        for k in range(200):
            continue
        rospy.loginfo('publishing 5,5')
        publisher(5, 5, 10)
        checking_goal_point(5, 5)

        for k in range(200):
            continue
        rospy.loginfo('publishing -5,5')
        publisher(-5, 5, 10)
        checking_goal_point(-5, 5)

        for k in range(200):
            continue
        rospy.loginfo('publishing -5,-5')
        publisher(-5, -5, 10)
        checking_goal_point(-5, -5)

        for k in range(200):
            continue
        rospy.loginfo('publishing 5,-5')
        publisher(5, -5, 10)
        checking_goal_point(5, -5)

        for k in range(200):
            continue
        rospy.loginfo('publishing 5,0')
        publisher(5, 0, 10)
        checking_goal_point(5, 0)

    except:
        pass
