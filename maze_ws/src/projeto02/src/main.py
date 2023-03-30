#! /usr/bin/python

import rospy
from time import sleep
from math import ceil, pi, asin
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class myRobot():

    def __init__(self):
        print('init')
        self.sub_od = rospy.Subscriber('/mobile_base_controller/odom', Odometry, self.callback_odometria, queue_size=1)
        self.sub_laser = rospy.Subscriber('/scan_raw', LaserScan, self.callback_laser, queue_size=1)
        self.laser_ranges = None
        self.n_laser = None
        # Client Service camera
        self.base_pub = rospy.Publisher('/nav_vel', Twist, queue_size=1)
        self.orientation = 0
        # Publisher cabeca

    def callback_odometria(self, msg: Odometry):
        # print('callback odometria')
        # Armazenar os dados de odometria
        q = msg.pose.pose.orientation
        self.orientation = euler_from_quaternion([q.x, q.y, q.z, q.w])[-1]
        print(self.orientation)
        pass
        

    def callback_laser(self, msg: LaserScan):
        # print('callback laser')
        # Armazenar os dados do laser
        self.laser_ranges = [x if x > 0.1 else float('inf') for x in msg.ranges]
        self.n_laser = ceil((msg.angle_max - msg.angle_min) / msg.angle_increment + 1)
        # print(self.laser_ranges)

    def move_straight(self):
        print('move straight')
        move = Twist()
        move.linear.x = 5
        self.base_pub.publish(move)
        
    def stop(self):
        move = Twist()
        self.base_pub.publish(move)

    def turn(self, angle):
        print('turn')
        self.stop()
        inital_ori = self.orientation % pi
        move = Twist()
        while abs((self.orientation % pi) - inital_ori) < pi/2:
            move.angular.z = 0.2
            self.base_pub.publish(move)
        print('-'*30)
        
    def turn_right(self):
        self.turn(pi)
        
    def decision(self):
        print('decision')
        if self.n_laser is None:
            return 0
        
        side = self.n_laser // 3
        
        right = min(self.laser_ranges[:side])
        # straight = min(self.laser_ranges[side:-side])
        left = min(self.laser_ranges[-side:])
        
        if right < 1.5 and left < 1.5:
            return 2  # Andar pra frente
        elif right >= 1.5 and left >= 1.5:
            return 1  # Tirar fotos
        elif left >= 1.5:
            return 3  # Virar para esquerda
        elif right >= 1.5:
            return 4  # Virar para direita
        else:
            return 0
            

if __name__ == '__main__':

    rospy.init_node('maze_runner')

    tiago = myRobot()
    
    # Executando laço 4 vezes por segundo
    rate = rospy.Rate(4)

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
            sleep(10)
            print('='*30)
            print(mean(tiago.laser_ranges[:222]))
            print('='*30)
            print(mean(tiago.laser_ranges[222:-222]))
            print('='*30)
            print(mean(tiago.laser_ranges[-222:]))
            #compute next state

        state = tiago.decision()
        
        tiago.turn(pi/2)
        break
        print(state)
        rate.sleep()