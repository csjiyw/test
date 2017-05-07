import rospy
import numpy as np
import json

import cv2
import cv_bridge
import baxter_interface


class Robot:
    def __init__(self):
        rospy.init_node('rsdk_xdisplay_image', anonymous=True)

        self.limb=baxter_interface.Limb('left')
