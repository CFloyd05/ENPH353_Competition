execute_process(COMMAND "/home/fizzer/ros_ws/build/imitation_learning_controller/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/fizzer/ros_ws/build/imitation_learning_controller/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
