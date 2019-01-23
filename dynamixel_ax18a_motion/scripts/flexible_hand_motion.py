#!/usr/bin/env python
# coding: UTF-8

#######################################################
#2018 12 6 作成　ver2-2ハンド(flexible hand)を動作させるためのソース
#著　阿部
#######################################################

import rospy
import math
import sys
from std_msgs.msg import Float64


N     = 0.5  #把持力を上げるための射出[mm]( about max = 5.5)
INJCTION_ANG = 50.0  #射出部の角度[deg]

up_limit_deg   = 90.0
down_limit_deg = -20.0

print '\n'*3 + '='*5 + ' start ' + '='*5
print N,'[mm]'

def callback(target_d):

    target_d_ = target_d.data           #対象部品の直径[mm]    print '\n'
    # print 'start'

    target_r_ = target_d_ * 0.5         #対象部品の半径[mm]
    injection_parts_r = 2.5             #射出部品半径[mm]
    injection_angle = (57*math.pi)/180  #射出部角度[rad]
    
    if target_d_<=5.0:
        # print 'go init'
        hand_r = target_r_
    else:
        hand_r = target_r_ + N       #ハンド半径[mm]

    
    injection_amount = (hand_r - injection_parts_r)/(math.sin(injection_angle))  #射出量[mm]
    axis_dire= injection_amount * math.cos(injection_angle)  #軸方向距離[mm]
    cam_displacement = injection_amount              #カム変位[mm]
    cam_rot_rad = (cam_displacement * math.pi)/14.0  #カム回転角度[rad]
    cam_rot_deg = (cam_rot_rad * 180.0)/math.pi


    if cam_rot_deg < down_limit_deg :
        print '\n','!'*7,'This degree(',cam_rot_deg,') is danger. So I fixed ',down_limit_deg,'[deg]','!'*7,'\n'
        # cam_rot_deg = down_limit_deg
        return
    elif cam_rot_deg > up_limit_deg:
        print '\n','!'*7,'This degree(',cam_rot_deg,') is danger. So I fixed ',up_limit_deg,'[deg]','!'*7,'\n'
        # cam_rot_deg = up_limit_deg
        return

    motor_rad_result = get_motor_rad(cam_rot_deg)
    
    if target_d_ > 5.0:
        print '対象物直径[mm]',round(target_d_,2),'半径[mm]',round(target_r_,2)
        print '爪射出量[mm]',round(injection_amount,2),'把持力向上射出距離',round(N,2)
        print '直径方向[mm]',round(hand_r*2,2),'爪軸方向[mm]',round(axis_dire,2)
        print 'カム角度[deg]=',round(cam_rot_deg,2), 'モータ角度[deg]=',round(motor_rad_result*180/math.pi,2)
        print '\n'

    pub.publish(motor_rad_result)
        


def listener():
    rospy.Subscriber('flexiblehand_motion_listener',Float64,callback)
    rospy.spin()



def get_motor_rad(cam_deg_):
    gear_motor_z = 32.0
    gear_cam_z  = 20.0
    reduction_ration = gear_motor_z / gear_cam_z
    motor_rad_ = ((cam_deg_ * math.pi)/180.0) * (1/reduction_ration)
    return motor_rad_
    


if __name__=='__main__':
    rospy.init_node('joint_motion',anonymous=True)
    pub = rospy.Publisher('tilt_controller/command',Float64,queue_size=10)
    r = rospy.Rate(10)
    
    listener()

