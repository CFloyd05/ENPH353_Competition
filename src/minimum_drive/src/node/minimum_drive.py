#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

rospy.init_node('topic_publisher')
sub = rospy.Subscriber('', String, clue_publish_callback, queue_size=1)
pub_vel = rospy.Publisher('/B1/cmd_vel', Twist, queue_size=1)
pub_clue = rospy.Publisher('/score_tracker', String, queue_size=1)

move = Twist()
clue = String()
DRIVE_SPEED = 3

# State 1: Startup
# State 2: read first board
# State 3: drive forward until second board is read
# Optional state 4: drive forward and read third sign on right
# State 5: Teleport to second line drive back and read fourth sign
# State 6: drive forward, read fifth sign behind
# State 7: read sixth sign to left
# State 8: teleport to tunnel, drive back and read seventh sign

state = 1

def clue_publish_callback(clue):
  if clue == 1:
    state = 3
  elif clue == 2:
    state = 4
  elif clue == 3:
    state = 5
  elif clue == 4:
    state = 6
  elif clue == 5:
    state = 7
  elif clue == 6:
    state = 8


while state = 1:
  rospy.sleep(1)
  clue = ('AIZCF,beans,0,letzgo')
  pub_clue.publish(clue)
  state = 2

while state = 2:
  move.linear.x = DRIVE_SPEED
  pub_vel.publish(move)
  

clue = ('AIZCF,beans,-1,letzstop')
move.linear.x = 0
pub_clue.publish(plate)
pub_vel.publish(move)

rospy.spin


