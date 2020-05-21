#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
import math as mt
import numpy as np
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from ik_front import ik as ikf
from ik_hind import ik as ikh

fpose = Pose2D()
hpose = Pose2D()
def callback(Pose2D, pose):
    rospy.loginfo(Pose2D)
    pose.x = Pose2D.x
    pose.y = Pose2D.y
    pose.theta = Pose2D.theta

def ik():
    pose = Pose2D()
    rospy.init_node('ik')
    rospy.Subscriber("front_pose", Pose2D, callback, fpose)
    rospy.Subscriber("hind_pose", Pose2D, callback, hpose)
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    #rospy.init_node('joint_state_publisher')
    pub2 = rospy.Publisher('front_joints', Pose2D, queue_size=3)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #front_joints_str = Pose2D
        rospy.loginfo(fpose)
        pub2.publish(fpose)
	q1, q2, q3, q4 = ikf(fpose.x,fpose.y,fpose.theta)
	qf, q5, q6, q7, q8 = ikh(hpose.x,hpose.y,hpose.theta)
	joint_str = JointState()
        joint_str.header = Header()
        joint_str.header.stamp = rospy.Time.now()
        joint_str.name = ['base_to_scapula', 'scapula_to_humerus', 'humerus_to_radius', 'radius_to_carpus', 'base_to_femur', 'femur_to_tibia', 'tibia_to_tarsus', 'tarsus_to_phalange']
        joint_str.position = [q1, q2, q3, q4, qf+q5, q6, q7, q8]
        joint_str.velocity = []
        joint_str.effort = []
        pub.publish(joint_str)
        rate.sleep()
	
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    ik()
