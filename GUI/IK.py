import rospy
import baxter_interface
from baxter_interface import CameraController
from sensor_msgs.msg import (
    Image,
)

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

import argparse

class myIK:
    def __init__(self):
        self.a=1

    def ik_test(self,limb,dx,dy,dz):
        ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
        iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
        ikreq = SolvePositionIKRequest()
        hdr = Header(stamp=rospy.Time.now(), frame_id='base')
        poses = {
            'left': PoseStamped(
                header=hdr,
                pose=Pose(
                    position=Point(
                        x=dx,
                        y=dy,
                        z=dz,
                    ),
                orientation=Quaternion(
                    x=1,
                    y=0,
                    z=0,
                    w=0,
                    ),
                ),
            ),
            'right': PoseStamped(
                header=hdr,
                pose=Pose(
                    position=Point(
                        x=0.656982770038,
                        y=-0.852598021641,
                        z=0.0388609422173,
                    ),
                    orientation=Quaternion(
                        x=0.367048116303,
                        y=0.885911751787,
                        z=-0.108908281936,
                        w=0.261868353356,
                    ),
                ),
            ),
        }

        ikreq.pose_stamp.append(poses[limb])
        try:
            rospy.wait_for_service(ns, 5.0)
            resp = iksvc(ikreq)
        except (rospy.ServiceException, rospy.ROSException), e:
            rospy.logerr("Service call failed: %s" % (e,))
            return 1

        if (resp.isValid[0]):
            #print("SUCCESS - Valid Joint Solution Found:")
            # Format solution into Limb API-compatible dictionary
            limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
            #print(limb_joints)
            return limb_joints,True

        else:
            print("INVALID POSE - No Valid Joint Solution Found.")
            return 0,False

        return 0
