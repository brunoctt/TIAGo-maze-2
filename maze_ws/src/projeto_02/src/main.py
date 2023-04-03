#! /usr/bin/python

import actionlib
import rospy
from time import sleep
from numpy import mean
from math import ceil, pi
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from projeto_02.srv import CameraRes, CameraResResponse
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint

class myRobot():

    distance = 1.2

    def __init__(self):
        print('init')
        self.sub_od = rospy.Subscriber('/mobile_base_controller/odom', Odometry, self.callback_odometria, queue_size=1)
        self.sub_laser = rospy.Subscriber('/scan_raw', LaserScan, self.callback_laser, queue_size=1)
        self.laser_ranges = None
        self.right = self.left = self.straight = None
        self.n_laser = None
        # Client Service camera
        self.base_pub = rospy.Publisher('/nav_vel', Twist, queue_size=1)
        self.orientation = None
        self.pub_head = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
        # Executando laço 10000 vezes por segundo
        self.rate = rospy.Rate(10000)

    def waving_hand(self):
        # Cria um objeto de ação de controle do braço do TIAGo
        arm_client = actionlib.SimpleActionClient("/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction)

        # Espera até que o servidor de ação esteja pronto
        arm_client.wait_for_server()

        # Definindo o nome das juntas
        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = ["arm_1_joint", "arm_2_joint", "arm_3_joint", 
                                    "arm_4_joint", "arm_5_joint", "arm_6_joint", "arm_7_joint"]
        #Definindo os pontos de trajetória 
        points = [[0.0, pi/2, 0.0, pi/4, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, -pi, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, pi/4, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, -pi, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, pi/4, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, -pi, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, pi/4, 0.0, 0.0, 0.0],
                [0.0, pi/2, 0.0, -pi, 0.0, 0.0, 0.0]]

        # Adiciona cada ponto de trajetória à mensagem de trajetória
        time_from_start = rospy.Duration(0.0)
        for point in points:
            joint_point = JointTrajectoryPoint()
            joint_point.positions = point
            joint_point.time_from_start = time_from_start
            arm_trajectory.points.append(joint_point)
            time_from_start += rospy.Duration(1.5) # Tempo de duração de cada ponto de trajetória

        # Cria uma meta de ação para controlar o braço do TIAGo com a mensagem de trajetória
        arm_goal = FollowJointTrajectoryGoal()
        arm_goal.trajectory = arm_trajectory

        # Envia a meta de ação para o servidor de ação do braço do TIAGo
        arm_client.send_goal(arm_goal)

        # Espera até que a ação seja concluída
        arm_client.wait_for_result()
    
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
        side = self.n_laser // 3
        self.right = mean(sorted(self.laser_ranges[:side])[:50])
        self.straight = mean(sorted(self.laser_ranges[side:-side])[:50])
        self.left = mean(sorted(self.laser_ranges[-side:])[:50])
        # print(self.laser_ranges)

    def move_straight(self):
        print('move straight')
        move = Twist()
        k_linear = 2
        k_angular = 0.6
        dist = 1
        while self.straight - dist > 0.005:
            move.linear.x = k_linear * (self.straight - dist)
            if abs(self.right - self.left) < 0.3:
                move.angular.z = k_angular * (self.left - self.right)
            else:
                move.angular.z = 0
            self.base_pub.publish(move)
            self.rate.sleep()
        
    def turn(self, angle):
        print('turn')
        while self.orientation is None:
            pass
        initial_ori = self.orientation
        move = Twist()
        diff = min(abs(self.orientation - initial_ori), (self.orientation - initial_ori)%pi)
        while diff < pi/2 - 0.03:
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
        
        print('-'*30)
        print(self.left)
        print(self.straight)
        print(self.right)
        if (self.right < self.distance and self.left < self.distance) or self.straight > 1.2:
            return 2  # Andar pra frente
        elif self.right >= self.distance and self.left >= self.distance:
            return 1  # Tirar fotos
        elif self.left >= self.distance:
            return 3  # Virar para esquerda
        elif self.right >= self.distance:
            return 4  # Virar para direita
        else:
            return 0
         
    def image_processing(self):
        # Virar a cabeca
        state = self.move_head()
        
        move = Twist()
        k_linear = 2
        dist = 0.7
        while self.straight - dist > 0.005:
            move.linear.x = k_linear * (self.straight - dist)
            self.base_pub.publish(move)
            self.rate.sleep()
        
        if state == 3:
            self.turn_left()
        elif state == 4:
            self.turn_right()
        elif state == 5:
            self.waving_hand()
            return True
            
        move = Twist()
        for _ in range(int(1e3)):
            move.linear.x = 2
            self.base_pub.publish(move)
            self.rate.sleep()
            
        return False
        
    def take_picture(self):
        rospy.wait_for_service('camera_result_service')
        try:
            # Connect to the server
            h_dist = rospy.ServiceProxy('camera_result_service', CameraRes)

            # Call the service
            response: CameraResResponse = h_dist()
            return response.res

        # If the connection fails (DEBUG)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return 3
    
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
        left = self.take_picture()
        self.rot_head_right(cmd)
        right = self.take_picture()
        # print(f"Left: {left}")
        # print(f"Right: {right}")
        if left == 0:
            return 3  # turn_left
        elif right == 0:
            return 4  # turn_right
        elif (right, left) == (2, 2):
            return 5  # end

    def rot_head_left(self, cmd):
        angle = 0.0
        while angle < pi:
            cmd.points[0].positions[0] = angle
            cmd.points[0].time_from_start = rospy.Duration(1)

            self.pub_head.publish(cmd)
            angle += pi/16
            self.rate.sleep()
            
    def rot_head_right(self, cmd):
        angle = 0.0
        while angle > -pi:
            cmd.points[0].positions[0] = angle
            cmd.points[0].time_from_start = rospy.Duration(1)

            self.pub_head.publish(cmd)
            angle -= pi/16
            self.rate.sleep()

if __name__ == '__main__':

    rospy.init_node('maze_runner')

    tiago = myRobot()
    # sleep(5)
    stop = False
    state = 0
    while (not rospy.is_shutdown()) and state != 5:
        prev = state
        if state == 0:
            pass
            #compute next state
        elif state == 1:
            stop = tiago.image_processing()
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
        if stop:
            state = 5
        print(state)
        tiago.rate.sleep()