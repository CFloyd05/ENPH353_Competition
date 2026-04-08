#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

rospy.init_node('drive_statemachine_controller')

move = Twist()
clue = String()
camera = String()
DRIVE_SPEED = 3
START_POSITION = [5.5, 2.4, 0.05, 0, 0, -0.7071, 0.7071] #yaw = -pi/2
LINE_1 = [0.5, -0.1, 0.05, 0, 0, 0.7071, 0.7071] #yaw = pi/2
LINE_2 = [-3.85, 0.45, 0.05, 0, 0, 1, 0] # yaw = pi
LINE_3 = [-4.1, -2.3, 0.05, 0, 0, 0, 1] #yaw = 0
rate = rospy.Rate(10)


def clue_publish_callback(clue_input):
  clue = clue_input.data()
  if clue == 1:
    print("Clue 1 found: Entering State 3")
    state3_start_time = rospy.Time.now()
    state = 3
  elif clue == 2:
    print("Clue 2 found: Entering State 4")
    state4_start_time = rospy.Time.now()
    state = 4
  elif clue == 3:
    print("Clue 3 found: Entering State 5")
    state5_start_time = rospy.Time.now()
    state = 5
  elif clue == 4:
    print("Clue 4 found: Entering State 7")
    state7_start_time = rospy.Time.now()
    state = 7
  elif clue == 5:
    print("Clue 5 found: Entering State 9")
    state9_start_time = rospy.Time.now()
    state = 9
  elif clue == 6:
    print("Clue 6 found: Entering State 8")
    state8_start_time = rospy.Time.now()
    state = 8
  elif clue == 7:
    print("Clue 7 found: Entering State 88")
    state88_start_time = rospy.Time.now()
    state = 88

def stop():
  move.linear.x = 0
  move.linear.y = 0
  move.linear.z = 0
  move.angular.x = 0
  move.angular.y = 0
  move.angular.z = 0
  pub_vel.publish(move)

def drive_forward(speed):
  move.linear.x = speed
  move.linear.y = 0
  move.linear.z = 0
  move.angular.x = 0
  move.angular.y = 0
  move.angular.z = 0
  pub_vel.publish(move)

def set_position(position):
        msg = ModelState()
        msg.model_name = 'B1'

        msg.pose.position.x = position[0]
        msg.pose.position.y = position[1]
        msg.pose.position.z = position[2]
        msg.pose.orientation.x = position[3]
        msg.pose.orientation.y = position[4]
        msg.pose.orientation.z = position[5]
        msg.pose.orientation.w = position[6]

        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            resp = set_state( msg )

        except rospy.ServiceException:
            print ("Service call failed")


# State machine overview
#
# State 1: start timer
# State 2: read first board
# State 3: drive forward and read second sign in front
# State 4: drive forward and read third sign on right
# State 5: teleport to second line
# State 6: drive back and read fourth sign
# State 7: drive forward, read sixth sign on left
# State 8: drive forward, read fifth sign behind
# State 9: teleport to tunnel
# State 10: drive back and read seventh sign
# State 11: line-follow up mountain
#
# State 88: end timer
# State 99: restart from state 1


# Pre-state machine startup
sub = rospy.Subscriber('clue_publish_updates', String, clue_publish_callback, queue_size=1)
pub_vel = rospy.Publisher('/B1/cmd_vel', Twist, queue_size=1)
pub_clue = rospy.Publisher('/score_tracker', String, queue_size=1)
pub_camera = rospy.Publisher('/camera_to_read', String, queue_size=1)

set_position(START_POSITION)
print("Entering State 1")
state1_start_time = rospy.Time.now()
state = 1


while not rospy.is_shutdown():

  # State 1: Startup
  # Exit: One loop completed (state 2)
  if state == 1:
    stop()
    pub_camera.publish('front')

    rospy.sleep(1)
    pub_clue.publish('AIZCF,beans,0,letzgo')

    print("Entering State 2")
    state2_start_time = rospy.Time.now()
    state = 2


  # State 2: Read first clue
  # Exit: First clue published to score tracker (state 3) || 5 seconds passed (state 3)
  if state == 2:
    stop()
    pub_camera.publish('front')
    elapsed = rospy.Time.now() - state2_start_time

    if elapsed.to_sec() > 5:
      print("Clue 1 not found: Entering state 3")
      state3_start_time = rospy.Time.now()
      state = 3


  # State 3: Drive forward and read second clue
  # Exit: Second clue published to score tracker (state 4) || 10 seconds passed (state 5)
  if state == 3:
    drive_forward(DRIVE_SPEED)
    pub_camera.publish('front')
    elapsed = rospy.Time.now() - state3_start_time

    if elapsed.to_sec() > 10:
      print("Clue 2 not found: Entering state 5")
      state5_start_time = rospy.Time.now()
      state = 5


  # State 4: Drive forward and read third clue on right
  # Exit: Third clue published to score tracker (state 5) || 10 seconds passed (state 5)
  if state == 4:
    drive_forward(DRIVE_SPEED)
    pub_camera.publish('right')
    elapsed = rospy.Time.now() - state4_start_time

    if elapsed.to_sec() > 10:
      print("Clue 2 not found: Entering state 5")
      state5_start_time = rospy.Time.now()
      state = 5


  # State 5: Teleport to first line
  # Exit: One loop completed (State 6)
  if state == 5:
    stop()
    set_position(LINE_1)
    print("Teleported to first line: Entering state 6")
    state6_start_time = rospy.Time.now()
    state = 6


  # State 6: Drive backwards and read fourth clue
  # Exit: Fourth clue published to score tracker (state 7) || 6 seconds passed (state 7)
  if state == 6:
    drive_forward(-DRIVE_SPEED)
    pub_camera.publish('front')
    elapsed = rospy.Time.now() - state6_start_time

    if elapsed.to_sec() > 10:
      print("Clue 4 not found: Entering state 7")
      state7_start_time = rospy.Time.now()
      state = 7


  # State 7: Drive forwards and read sixth clue on left
  # Exit: Sixth clue published to score tracker (state 8) || 15 seconds passed (state 8)
  if state == 7:
    drive_forward(DRIVE_SPEED)
    pub_camera.publish('left')
    elapsed = rospy.Time.now() - state7_start_time

    if elapsed.to_sec() > 15:
      print("Clue 6 not found: Entering state 8")
      state8_start_time = rospy.Time.now()
      state = 8


  # State 8: Drive forwards and read fifth clue behind
  # Exit: Fifth clue published to score tracker (state 9) || 10 seconds passed (state 9)
  if state == 8:
    drive_forward(DRIVE_SPEED)
    pub_camera.publish('rear')
    elapsed = rospy.Time.now() - state7_start_time

    if elapsed.to_sec() > 10:
      print("Clue 5 not found: Entering state 9")
      state9_start_time = rospy.Time.now()
      state = 9


  # State 9: Teloport to tunnel
  # Exit: One loop completed (State 10)
  if state == 9:
    stop()
    set_position(LINE_3)
    print("Teleported to tunnel: Entering state 10")
    state10_start_time = rospy.Time.now()
    state = 10


  # State 10: Drive backwards and read seventh sign
  # Exit: Seventh clue published to score tracker (state 88) || 5 seconds passed (state 88)
  if state == 10:
    drive_forward(DRIVE_SPEED)
    pub_camera.publish('front')
    elapsed = rospy.Time.now() - state7_start_time

    if elapsed.to_sec() > 10:
      print("Clue 7 not found: Entering state 88")
      state88_start_time = rospy.Time.now()
      state = 88


  # State 88: Stop robot and timer
  # Exit: none
  if state == 88:
    stop()
    pub_clue.publish('AIZCF,beans,-1,letzstop')
    state = 0


  # State 99: Reset robot from beginning
  if state == 99:
    stop()
    pub_camera.publish('front')
    set_position(START_POSITION)
    print("Restarting: Entering State 1")
    state1_start_time = rospy.Time.now()
    state = 1


  rate.sleep()
