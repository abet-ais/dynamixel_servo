#!/usr/bin/env python
# coding: UTF-8

#######################################################
#2019 1 20 作成　flexiblehandを動かすためのソース(穴の直径を送る)
#著　阿部
#######################################################

import rospy
import math
import sys
import time
from std_msgs.msg import Float64

publish_time    = 1.0   #publishする時間[s]
grasp_wait_time = 5.0   #把持している間の時間[s]


def send_hole_diameter_(diameter):

    diameter_ = Float64()
    diameter_.data =  diameter


    t1 = time.time()
    t2 = t1
    while (t2-t1) <= publish_time:
        pub.publish(diameter_)
        t2 = time.time()
        r.sleep()
            
    # time.sleep(grasp_wait_time)
    print raw_input('Enterを押してください')
            
    t1 = time.time()
    t2 = t1
    diameter_.data = 4.0
    while (t2-t1) <= publish_time:
        pub.publish(diameter_)
        t2 = time.time()
        r.sleep()

        
if __name__=='__main__':
    print 'start'
    rospy.init_node('send_hole_diameter',anonymous=True)
    pub = rospy.Publisher('flexiblehand_motion_listener',Float64,queue_size=10)
    r = rospy.Rate(10)

    args = sys.argv

    print '対象物穴直径',args[1],'[mm]'
    send_hole_diameter_(float(args[1]))

    print 'end','\n'

