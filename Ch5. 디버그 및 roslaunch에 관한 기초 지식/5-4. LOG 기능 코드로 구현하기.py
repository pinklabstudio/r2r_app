import rclpy as rp
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

import time
import math

from my_first_package_msgs.action import DistTurtle
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_first_package.my_subscriber import TurtlesimSubscriber

from rcl_interfaces.msg import SetParametersResult

class TurtleSub_Action(TurtlesimSubscriber):
    def __init__(self, ac_server):
       super().__init__()
       self.ac_server = ac_server
       
    def callback(self, msg):
        self.ac_server.current_pose = msg

class DistTurtleServer(Node):

    def __init__(self):
        super().__init__('dist_turtle_action_server')
        self.total_dist = 0.0
        self.is_first_time = True
        self.current_pose = Pose()
        self.previous_pose = Pose()
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.action_server = ActionServer(self, DistTurtle, 'dist_turtle', self.execute_callback)

        self.get_logger().info("DistTurtle action server has been started.")

        self.declare_parameter('quantile_time', 0.75)
        self.declare_parameter('almost_goal_time', 0.95)


        (quantile_time, almost_goal_time) = self.get_parameters(
                                        ['quantile_time', 'almost_goal_time'])
        
        
        self.quantile_time = quantile_time.value
        self.almost_goal_time = almost_goal_time.value

        output_msg = "Quantile time is " + str(self.quantile_time)
        output_msg += output_msg + " and almost goal time is " + str(self.almost_goal_time)
        self.get_logger().info(output_msg)
        
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            print(param.name, " is changed to ", param.value)

            if param.name == 'quantile_time':
                self.quantile_time = param.value
            if param.name == 'almost_goal_time':
                self.almost_goal_time = param.value

        output_msg = "Quantile time is " + str(self.quantile_time)
        output_msg = output_msg + " and almost goal time is " + str(self.almost_goal_time)
        self.get_logger().info(output_msg)

        return SetParametersResult(successful=True)

    def calc_diff_pose(self):
        if self.is_first_time:
            self.previous_pose.x = self.current_pose.x
            self.previous_pose.y = self.current_pose.y
            self.is_first_time = False

        diff_pose = math.sqrt((self.current_pose.x - self.previous_pose.x)**2 +\
                                (self.current_pose.y - self.previous_pose.y)**2)
        
        self.previous_pose = self.current_pose

        return diff_pose

    def execute_callback(self, goal_handle):
        feedback_msg = DistTurtle.Feedback()
        
        msg = Twist()
        msg.linear.x = goal_handle.request.linear_x
        msg.angular.z = goal_handle.request.angular_z

        while True:
            self.total_dist += self.calc_diff_pose()
            feedback_msg.remained_dist = goal_handle.request.dist - self.total_dist
            goal_handle.publish_feedback(feedback_msg)
            self.publisher.publish(msg)
            
            tmp = feedback_msg.remained_dist - goal_handle.request.dist * self.quantile_time
            tmp = abs(tmp)

            if tmp < 0.02:
                output_msg = "The turtle passes the " + str(self.quantile_time) + " point."
                output_msg = output_msg + " : " + str(tmp)
                self.get_logger().info(output_msg)
            
            time.sleep(0.1)

            if feedback_msg.remained_dist < 0.2:
                break
        
        goal_handle.succeed()
        result = DistTurtle.Result()

        result.pos_x = self.current_pose.x
        result.pos_y = self.current_pose.y
        result.pos_theta = self.current_pose.theta
        result.result_dist = self.total_dist

        self.total_dist = 0.0
        self.is_first_time = True

        return result
    
def main(args=None):
    rp.init(args=args)
    
    executor = MultiThreadedExecutor()
    ac = DistTurtleServer()
    sub = TurtleSub_Action(ac_server=ac)

    executor.add_node(ac)
    executor.add_node(sub)

    try:
        executor.spin()
    
    finally:
        executor.shutdown()
        ac.destroy_node()
        sub.destroy_node()
        rp.shutdown()

if __name__ == '__main__':
    main()
