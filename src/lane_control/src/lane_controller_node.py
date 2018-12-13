#!/usr/bin/env python
import rospy
import numpy as np
import math
from duckietown_msgs.msg import  Twist2DStamped, LanePose
from duckietown_msgs.srv import SetParam

class lane_controller(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        self.lane_reading = None

        self.pub_counter = 0

        #track previous d error
        self.prev_de = 0
        #self.filter_tune = 0.8 #0.75
        # Setup parameters
        self.setGains()

        # Publicaiton
        self.pub_car_cmd = rospy.Publisher("~car_cmd",Twist2DStamped,queue_size=1)

        # Subscriptions
        self.sub_lane_reading = rospy.Subscriber("~lane_pose", LanePose, self.cbPose, queue_size=1)

        # safe shutdown
        rospy.on_shutdown(self.custom_shutdown)

        # timer
        self.gains_timer = rospy.Timer(rospy.Duration.from_sec(1.0), self.getGains_event)
        rospy.loginfo("[%s] Initialized " %(rospy.get_name()))

    def setupParameter(self,param_name,default_value):
        value = rospy.get_param(param_name,default_value)
        rospy.set_param(param_name,value) #Write to parameter server for transparancy
        rospy.loginfo("[%s] %s = %s " %(self.node_name,param_name,value))
        return value

    def setGains(self):
        v_bar = 0.25
        k_theta = -1.9 #-1.9
        k_d = - (k_theta ** 2) / ( 5.5 * v_bar)
        theta_thres = math.pi / 2 #I don't think this variable is used
        d_thres = math.fabs(k_theta / k_d) * theta_thres
        d_offset = -.3 #-0.05

        self.v_bar = self.setupParameter("~v_bar",v_bar) # Linear velocity
        self.k_d = self.setupParameter("~k_d",k_theta) # P gain for theta
        self.k_theta = self.setupParameter("~k_theta",k_d) # P gain for d
        self.d_thres = self.setupParameter("~d_thres",theta_thres) # Cap for error in d
        self.theta_thres = self.setupParameter("~theta_thres",d_thres) # Maximum desire theta
        self.d_offset = self.setupParameter("~d_offset",d_offset) # a configurable offset from the lane position

    def getGains_event(self, event):
        v_bar = rospy.get_param("~v_bar")
        k_d = rospy.get_param("~k_d")
        k_theta = rospy.get_param("~k_theta")
        d_thres = rospy.get_param("~d_thres")
        theta_thres = rospy.get_param("~theta_thres")
        theta_thres = rospy.get_param("~theta_thres")
        d_offset = rospy.get_param("~d_offset")

        params_old = (self.v_bar,self.k_d,self.k_theta,self.d_thres,self.theta_thres, self.d_offset)
        params_new = (v_bar,k_d,k_theta,d_thres,theta_thres, d_offset)

        if params_old != params_new:
            rospy.loginfo("[%s] Gains changed." %(self.node_name))
            rospy.loginfo("old gains, v_var %f, k_d %f, k_theta %f, theta_thres %f, d_thres %f, d_offset %f" %(params_old))
            rospy.loginfo("new gains, v_var %f, k_d %f, k_theta %f, theta_thres %f, d_thres %f, d_offset %f" %(params_new))
            self.v_bar = v_bar
            self.k_d = k_d
            self.k_theta = k_theta
            self.d_thres = d_thres
            self.theta_thres = theta_thres
            self.d_offset = d_offset

    def custom_shutdown(self):
        rospy.loginfo("[%s] Shutting down..." %self.node_name)
        # Stop listening
        self.sub_lane_reading.unregister()

        # Send stop command
        car_control_msg = Twist2DStamped()
        car_control_msg.v = 0.0
        car_control_msg.omega = 0.0
        self.publishCmd(car_control_msg)
        rospy.sleep(0.5) #To make sure that it gets published.
        rospy.loginfo("[%s] Shutdown" %self.node_name)


    def publishCmd(self,car_cmd_msg):
        self.pub_car_cmd.publish(car_cmd_msg)
 
    def cbPose(self,lane_pose_msg):
        self.lane_reading = lane_pose_msg
        cross_track_err = lane_pose_msg.d - self.d_offset
        #tuning
        #cross_track_err = self.filter_tune*(cross_track_err+self.d_offset)+(1-self.filter_tune)*self.prev_de
        #update
        self.prev_de = cross_track_err
        #true cross_track_error
        #cross_track_err = cross_track_err - self.d_offset


        heading_err = lane_pose_msg.phi

        car_control_msg = Twist2DStamped()
        car_control_msg.header = lane_pose_msg.header
        car_control_msg.v = self.v_bar #*self.speed_gain #Left stick V-axis. Up is positive
        
        #if math.fabs(cross_track_err) > self.d_thres:
            #if cross_track_err < 0: 
	        #rospy.loginfo("negative")
	    #else:
                #rospy.loginfo("positive")
            #cross_track_err = cross_track_err / math.fabs(cross_track_err) * self.d_thres
        car_control_msg.omega =  self.k_d * cross_track_err*1.8 + self.k_theta * heading_err*1.375 #*self.steer_gain #Right stick H-axis. Right is negative
        
        self.publishCmd(car_control_msg)

if __name__ == "__main__":
    rospy.init_node("lane_controller",anonymous=False)
    lane_control_node = lane_controller()
    rospy.spin()

