#! /usr/bin/python

import rospy
from time import sleep
from math import ceil, pi, asin
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class myRobot():

    distance = 1

    def __init__(self):
        print('init')
        self.sub_od = rospy.Subscriber('/mobile_base_controller/odom', Odometry, self.callback_odometria, queue_size=1)
        self.sub_laser = rospy.Subscriber('/scan_raw', LaserScan, self.callback_laser, queue_size=1)
        self.laser_ranges = None
        self.n_laser = None
        # Client Service camera
        self.base_pub = rospy.Publisher('/nav_vel', Twist, queue_size=1)
        self.orientation = None
        self.pub_head = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
        # Executando laço 4 vezes por segundo
        self.rate = rospy.Rate(4)

    def callback_odometria(self, msg: Odometry):
        # print('callback odometria')
        # Armazenar os dados de odometria
        q = msg.pose.pose.orientation
        self.orientation = round(euler_from_quaternion([q.x, q.y, q.z, q.w])[-1], 2)

    def callback_laser(self, msg: LaserScan):
        # print('callback laser')
        # Armazenar os dados do laser
        self.laser_ranges = [x if x > 0.1 else float('inf') for x in msg.ranges]
        self.n_laser = ceil((msg.angle_max - msg.angle_min) / msg.angle_increment + 1)
        # print(self.laser_ranges)

    def move_straight(self):
        print('move straight')
        move = Twist()
        dist_min_central = min(self.laser_ranges[222:-222])
        k = 2
        dist = 1
        move.linear.x = k * (dist_min_central - dist)
        self.base_pub.publish(move)
        
    def stop(self):
        move = Twist()
        self.base_pub.publish(move)

    def turn(self, angle):
        print('turn')
        self.stop()
        while self.orientation is None:
            pass
        initial_ori = self.orientation
        move = Twist()
        diff = min(abs(self.orientation - initial_ori), (self.orientation - initial_ori)%pi)
        while diff < pi/2 - 0.02:
            move.angular.z = (abs(angle) - diff) * (angle//abs(angle))
            self.base_pub.publish(move)
            diff = min(abs(self.orientation - initial_ori), (self.orientation - initial_ori)%pi)
        
    def turn_right(self):
        self.turn(-pi/2)
        
    def turn_left(self):
        self.turn(pi/2)
        
    def decision(self):
        print('decision')
        if self.n_laser is None:
            return 0
        
        side = self.n_laser // 3
        
        right = min(self.laser_ranges[:side])
        straight = min(self.laser_ranges[side:-side])
        left = min(self.laser_ranges[-side:])
        print('-'*30)
        print(left)
        print(straight)
        print(right)
        if (right < self.distance and left < self.distance) or straight > 1.2:
            return 2  # Andar pra frente
        elif right >= self.distance and left >= self.distance:
            return 1  # Tirar fotos
        elif left >= self.distance:
            return 3  # Virar para esquerda
        elif right >= self.distance:
            return 4  # Virar para direita
        else:
            return 0
         
    def image_processing(self):
        # Virar a cabeca
        self.move_head()
        
    def move_head(self):
        cmd = JointTrajectory()
        cmd.joint_names.append("head_1_joint")
        cmd.joint_names.append("head_2_joint")

        point = JointTrajectoryPoint()
        point.positions = [0] * 2
        point.velocities = [0] * 2
        point.accelerations = [0] * 2
        point.time_from_start = rospy.Duration(1)

        cmd.points.append(point)
        
        self.rot_head_left(cmd)
        self.rot_head_right(cmd)

    def rot_head_left(self, cmd):
        angle = 0.0
        while angle < 1.6:
            cmd.points[0].positions[0] = angle
            cmd.points[0].time_from_start = rospy.Duration(1)

            self.pub_head.publish(cmd)
            angle += 0.2
            self.rate.sleep()
            
    def rot_head_right(self, cmd):
        angle = 0.0
        while angle > -1.6:
            cmd.points[0].positions[0] = angle
            cmd.points[0].time_from_start = rospy.Duration(1)

            self.pub_head.publish(cmd)
            angle -= 0.2
            self.rate.sleep()

if __name__ == '__main__':

    rospy.init_node('maze_runner')

    tiago = myRobot()
    sleep(5)
    
    state = 0
    while not rospy.is_shutdown():
        if state == 0:
            pass
            #compute next state
        elif state == 1:
            tiago.image_processing()
            #compute next state
        elif state == 2:
            tiago.move_straight()
            #compute next state
        elif state == 3:
            tiago.turn_left()
            #compute next state
        elif state == 4:
            tiago.turn_right()
            #compute next state

        state = tiago.decision()
        
        # tiago.turn(pi/2)
        # break
        print(state)
        tiago.rate.sleep()