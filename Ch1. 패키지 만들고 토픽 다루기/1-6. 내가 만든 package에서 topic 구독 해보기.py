import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtlesimSubscriber(Node):
    def __init__(self):
        super().__init__('turtlesim_subscriber')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.callback,
            10
        )

    def callback(self, msg):
        print(("X: ", msg.x, "Y: ", msg.y))


def main():
    rp.init()

    turtlesim_subscriber = TurtlesimSubscriber()
    rp.spin(turtlesim_subscriber)

    turtlesim_subscriber.destroy_node()
    rp.shutdown()

if __name__ == '__main__':
    main()