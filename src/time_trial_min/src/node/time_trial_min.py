#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

rospy.init_node('topic_publisher')
pub_vel = rospy.Publisher('/B1/cmd_vel', Twist, queue_size=1)
pub_plate = rospy.Publisher('/score_tracker', String, queue_size=1)

rospy.sleep(1)

rate = rospy.Rate(0.5)
move = Twist()
plate = String()

plate = ('AIZCF,beans,0,letzgo')
move.linear.x = 1
pub_plate.publish(plate)
pub_vel.publish(move)

rospy.sleep(6)

plate = ('AIZCF,beans,-1,letzstop')
move.linear.x = 0
pub_plate.publish(plate)
pub_vel.publish(move)

rospy.spin
