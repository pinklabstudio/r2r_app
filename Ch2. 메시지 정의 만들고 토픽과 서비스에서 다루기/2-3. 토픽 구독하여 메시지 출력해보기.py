import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose

class CmdAndPose(Node):
    def __init__(self):
        super().__init__('turtleo_cmd_pose')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.callback_pose,
            10
        )

    def callback_pose(self, msg):
        print(msg)


def main():
    rp.init()

    turtlesim_subscriber = CmdAndPose()
    rp.spin(turtlesim_subscriber)

    turtlesim_subscriber.destroy_node()
    rp.shutdown()

if __name__ == '__main__':
    main()
