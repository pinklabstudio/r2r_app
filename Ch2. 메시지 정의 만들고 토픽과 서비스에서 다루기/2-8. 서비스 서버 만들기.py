from my_first_package_msgs.srv import MultiSpawn

import rclpy as rp
from rclpy.node import Node

class MultiSpawning(Node):
    def __init__(self):
        super().__init__('multi_spawn')
        self.server = self.create_service(MultiSpawn, "multi_spawn", self.callback_service)

    def callback_service(self, request, response):
        print('Request : ', request)

        response.x = [1., 2., 3.]
        response.y = [1., 20., 30.]
        response.theta = [100., 200., 300.]

        return response
    
def main(args=None):
    rp.init(args=args)
    MultiSpawn = MultiSpawning()
    rp.spin(MultiSpawn)
    rp.shutdown()
