#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Control de Robot Gato
---------------------------
Mover hacia adelante:        w
Mover hacia atrás:            x
Mover hacia la izquierda:     a
Mover hacia la derecha:       d
Detener movimiento:           espacio

CTRL-C para salir
"""

moveBindings = {
    'w':(1,0),
    'x':(-1,0),
    'a':(0,1),
    'd':(0,-1),
    ' ':(0,0)
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

settings = termios.tcgetattr(sys.stdin)

if __name__=="__main__":
    rospy.init_node('keyboard_control')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    twist = Twist()

    try:
        print(msg)
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                twist.linear.x = moveBindings[key][0]
                twist.angular.z = moveBindings[key][1]
            else:
                twist.linear.x = 0
                twist.angular.z = 0
            pub.publish(twist)
    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        pub.publish(twist)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
