#!/usr/bin/env python

import rospy
import actionlib

from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)
from trajectory_msgs.msg import (
    JointTrajectory,
    JointTrajectoryPoint,
)


def waving_hand():
    # Inicializa o nó do ROS
    rospy.init_node("waving_hand")

    # Cria um objeto de ação de controle do braço do TIAGo
    arm_client = actionlib.SimpleActionClient(
        "/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction
    )

    # Espera até que o servidor de ação esteja pronto
    rospy.loginfo("Esperando pelo servidor de ação...")
    arm_client.wait_for_server()

    # Cria uma mensagem de trajetória conjunta para controlar o braço do TIAGo
    arm_trajectory = JointTrajectory()
    arm_trajectory.joint_names = ["arm_1_joint", "arm_2_joint", "arm_3_joint", "arm_4_joint", "arm_5_joint", "arm_6_joint", "arm_7_joint"]

    # Define os pontos de trajetória para a ação de aceno
    points = [
        [1.57, 1.57, 0.0, 0.0, 0.0, -1.57, 0.0],
        [1.57, 1.57, 0.0, 0.0, 0.0, -1.57, 1.57],
        [1.57, 1.57, 0.0, 0.0, 0.0, -1.57, 0.0],
        [1.57, 1.57, 0.0, 0.0, 0.0, -1.57, 1.57],
        [1.57, 1.57, 0.0, 0.0, 0.0, -1.57, 0.0],
    ]

   # Adiciona cada ponto de trajetória à mensagem de trajetória
    time_from_start = rospy.Duration(0.0)
    for point in points:
        joint_point = JointTrajectoryPoint()
        joint_point.positions = point
        joint_point.time_from_start = time_from_start
        arm_trajectory.points.append(joint_point)
        time_from_start += rospy.Duration(2.0) # aumenta o tempo_from_start em 2 segundos a cada ponto de trajetória

    # Cria uma meta de ação para controlar o braço do TIAGo com a mensagem de trajetória
    arm_goal = FollowJointTrajectoryGoal()
    arm_goal.trajectory = arm_trajectory

    # Envia a meta de ação para o servidor de ação do braço do TIAGo
    rospy.loginfo("Acenando...")
    arm_client.send_goal(arm_goal)

    # Espera até que a ação seja concluída
    arm_client.wait_for_result()
    rospy.loginfo("Terminado!")


if __name__ == "__main__":
    try:
        waving_hand()
    except rospy.ROSInterruptException:
        pass