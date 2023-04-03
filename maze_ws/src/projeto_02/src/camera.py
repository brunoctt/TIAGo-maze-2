#! /usr/bin/python

import rospy
import cv2
from time import sleep
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from projeto_02.srv import CameraRes, CameraResResponse

class myCamera():

    def __init__(self):
        print('init camera')
        # Bridge to convert ROS message to openCV
        self.bridge = CvBridge()

        # Subscriber to the camera image
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_color",Image,self.callback_SubscribeCamera)

        # Server Service camera
        self.service = rospy.Service('camera_result_service', CameraRes, self.callback_ServiceCamera)
        
    def callback_ServiceCamera(self, request):
        # print('image service')
        sleep(2)
        
        # Extract the color layers
        blue = self.cv_image[:,:,0]
        green = self.cv_image[:,:,1]
        red = self.cv_image[:,:,2]
        
        red_amount = green_amount = 0
        thresh = 75
        
        for i in range(0, red.shape[0], 4):
            for j in range(0, red.shape[1], 4):
                if red[i][j] > thresh and green[i][j] < thresh and blue[i][j] < thresh:
                    red_amount += 1
                elif green[i][j] > thresh and red[i][j] < thresh and blue[i][j] < thresh:
                    green_amount += 1

        if (red_amount, green_amount) == (0, 0):
            result = 2  # Fim do labirinto
        elif red_amount > 0 and green_amount == 0:
            result = 1  # Encontrou vermelho
        elif red_amount == 0 and green_amount > 0:
            result = 0  # Encontrou verde
        else:
            result = 3  # Problema
        print(result)
        return result

    def callback_SubscribeCamera(self, msg):
        # print('callback camera')
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print(e)

        # cv_image[linha][coluna][bgr] bgr-> 0:blue, 1:green, 2:red
        # print(self.cv_image[0][0])
        # print(self.cv_image[0][0][0])


if __name__ == '__main__':

    rospy.init_node('maze_camera')

    cam = myCamera()

    rospy.spin()