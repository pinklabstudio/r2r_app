from my_first_package_msgs.srv import MultiSpawn
from turtlesim.srv import TeleportAbsolute

import rclpy as rp
from rclpy.node import Node

class MultiSpawning(Node):
    def __init__(self):
        super().__init__('multi_spawn')
        self.server = self.create_service(MultiSpawn, "multi_spawn", self.callback_service)
        self.teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.req_teleport = TeleportAbsolute.Request()

    def callback_service(self, request, response):
        self.req_teleport.x = 1.
        self.req_teleport.y = 1.
        self.teleport.call_async(self.req_teleport)

        return response
    
def main(args=None):
    rp.init(args=args)
    multi_spwan = MultiSpawning()
    rp.spin(multi_spwan)
    rp.shutdown()
