import rospy
import difflib
from std_msgs.msg import String

clue = String()
pub = rospy.Publisher('/score_tracker', String, queue_size=1)
pub_for_state = rospy.Publisher('/clue_publish_updates', String, queue_size=1)

clue_location = -2
types = ["SIZE", "VICTIM", "CRIME", "TIME", "LAB", "MOTIVE", "WEAPON", "BANDIT"]

def publish_clue(clue_type,clue_value)
  clue_type_actual = difflib.get_close_matches(clue_type, types, n=1)
  clue_type = clue_type_actual[0]

  if clue_type == 'SIZE':
    clue_location = 1
  elif clue_type == 'VICTIM'
    clue_location = 2
  elif clue_type == 'CRIME'
    clue_location = 3
  elif clue_type == 'TIME'
    clue_location = 4
  elif clue_type == 'LAB'
    clue_location = 5
  elif clue_type == 'MOTIVE'
    clue_location = 6
  elif clue_type == 'WEAPON'
    clue_location = 7
  elif clue_location = 'BANDIT'
    clue_location = 8
  else
    print("Clue read bad, womp womp")
    return("Bad clue read")

  clue = ("AIZCF", "beans", clue_location, clue_value)
  pub.publish(clue)
  pub_for_state(clue_location)
  return("Good clue read")
