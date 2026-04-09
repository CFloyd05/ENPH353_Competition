import rospy
import difflib
from std_msgs.msg import String
from std_msgs.msg import Int32

clue_location = String()
clue_value = String()
clue_output = String()
pub = rospy.Publisher('/score_tracker', String, queue_size=1)
pub_for_state = rospy.Publisher('/clue_publish_updates', Int32, queue_size=1)

clue_location = -2
types = ["SIZE", "VICTIM", "CRIME", "TIME", "LAB", "MOTIVE", "WEAPON", "BANDIT"]

def publish_clue(clue_type,clue_value):
  clue_type_actual = difflib.get_close_matches(clue_type, types, n=1)
  
  if len(clue_type_actual) == 0: # If the clue type is not recognized, we publish a bad clue read and return
    print("Clue read bad, womp womp")
    return("Bad clue read")
  clue_type = clue_type_actual[0]

  if clue_type == 'SIZE':
    clue_location = '1'
  elif clue_type == 'VICTIM':
    clue_location = '2'
  elif clue_type == 'CRIME':
    clue_location = '3'
  elif clue_type == 'TIME':
    clue_location = '4'
  elif clue_type == 'LAB':
    clue_location = '5'
  elif clue_type == 'MOTIVE':
    clue_location = '6'
  elif clue_type == 'WEAPON':
    clue_location = '7'
  elif clue_type == 'BANDIT':
    clue_location = '8'
  else:
    print("Clue read bad, womp womp")
    return("Bad clue read")

  clue_output = "AIZCF, beans, " + clue_location + ", " +  clue_value
  print(clue_output) # For troubleshooting
  pub.publish(clue_output)
  pub_for_state.publish(clue_location)
  return("Good clue read")
