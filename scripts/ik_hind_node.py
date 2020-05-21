#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard pose at %s", data.data)
    
def ik_hind_pose():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('ik_hind')
    rospy.Subscriber("hind_pose", String, callback)
    pub = rospy.Publisher('hind_joints', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hind_joints_str = "hind joints are: %s" % rospy.get_time()
        rospy.loginfo(hind_joints_str)
        pub.publish(hind_joints_str)
        rate.sleep()
	
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    ik_hind_pose()
