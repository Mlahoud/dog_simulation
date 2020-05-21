#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
import math as mt
import numpy as np

def generator():
    f_pose = rospy.Publisher('front_pose', Pose2D,queue_size=1)
    h_pose = rospy.Publisher('hind_pose', Pose2D,queue_size=1)
    rospy.init_node('generator')
    rate = rospy.Rate(10) # 10hz
    p0f = np.array([0, -140])
    p0h = np.array([0, -130])
    r = 30
    R = 2
    i = 0
    theta = np.linspace(2*mt.pi, 0, num=100)
    
    while not rospy.is_shutdown():
	cmd1 = Pose2D()
	cmd2 = Pose2D()
	cmd1.x = (p0f[0] + r * mt.cos(theta[i]))
	cmd2.x = (p0h[0] + r * mt.cos(theta[i]+mt.pi))
	cmd1.y = (p0f[1] + R * mt.sin(theta[i]))
	cmd2.y = (p0h[1] + R * mt.sin(theta[i]+mt.pi))
	cmd1.theta = mt.pi/10*mt.cos(theta[i]+mt.pi)
	cmd2.theta = mt.pi/10*mt.cos(theta[i])
        f_pose.publish(cmd1)
        h_pose.publish(cmd2)
	if (i > 98):
		i = 0
	else:
		i = i + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        generator()
    except rospy.ROSInterruptException:
        pass
