#!/usr/bin/env python3
import cv2
import rospy
import math
from geometry_msgs.msg import Twist
# for publishing velocity
velocity = Twist()

# using the MIL tracker
tracker = cv2.TrackerMIL_create()

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

roi = cv2.selectROI(frame, False)

ret = tracker.init(frame, roi)

# calculating width and height to calculate the midpoint of the whole frame
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# calculating the midpoint of the frame
screen_mid_x = width/2
screen_mid_y = height/2

rospy.init_node('vel_publisher', anonymous=True)
pub = rospy.Publisher(
    '/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10)


def publisher(x, y):

    global screen_mid_x, screen_mid_y, velocity

    # iam defining cos and sin of the midpoint of rectangle tracked relative to the screen midpoint
    cos = abs((x-screen_mid_x) /
              (math.sqrt((x-screen_mid_x)**2 + (y-screen_mid_y)**2)))
    sin = abs((y-screen_mid_y) /
              (math.sqrt((x-screen_mid_x)**2 + (y-screen_mid_y)**2)))
    # here i am publishing velocity according to the midpoint of rectangle tracked relative to the screen midpoint
    if (x-screen_mid_x) > 0 and (y-screen_mid_y) > 0:
        velocity.linear.x = 0
        velocity.linear.y = cos*20
        velocity.linear.z = -sin*20
        pub.publish(velocity)
        rospy.loginfo(
            f'velocity is ( {velocity.linear.y}, {velocity.linear.z} )')

    if (x-screen_mid_x) > 0 and (y-screen_mid_y) < 0:
        velocity.linear.x = 0
        velocity.linear.y = cos*20
        velocity.linear.z = sin*20
        pub.publish(velocity)
        rospy.loginfo(
            f'velocity is ( {velocity.linear.y}, {velocity.linear.z} )')

    if (x-screen_mid_x) < 0 and (y-screen_mid_y) < 0:
        velocity.linear.x = 0
        velocity.linear.y = -cos*20
        velocity.linear.z = sin*20
        pub.publish(velocity)
        rospy.loginfo(
            f'velocity is ( {velocity.linear.y}, {velocity.linear.z} )')

    if (x-screen_mid_x) > 0 and (y-screen_mid_y) < 0:
        velocity.linear.x = 0
        velocity.linear.y = -cos*20
        velocity.linear.z = -sin*20
        pub.publish(velocity)
        rospy.loginfo(
            f'velocity is ( {velocity.linear.y}, {velocity.linear.z} )')


while True:

    ret, frame = cap.read()

    success, roi = tracker.update(frame)

    (x, y, w, h) = tuple(map(int, roi))

    if success:
        # p1 and p2 are for calculating the midpoint of the rectangle that is tracked
        p1 = (x, y)
        p2 = (x+w, y+h)
        print(f'p1 = {p1} and p2 = {p2}')
        frame_mid_x = (p1[0]+p2[0])/2
        frame_mid_y = (p1[1]+p2[1])/2

        publisher(frame_mid_x, frame_mid_y)

        cv2.rectangle(frame, p1, p2, (0, 0, 255), 3)

    else:

        cv2.putText(frame, "failued to detect", (100, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imshow('tracking', frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
