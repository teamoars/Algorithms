import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import json
import random

class GraphPublisher(Node):

    def __init__(self):
        super().__init__('graph_publisher')
        self.publisher_ = self.create_publisher(String, 'graph_topic', 10)
        self.graph = np.zeros((16, 16), dtype=int)  # Initialize empty graph
        self.target = (random.randint(0, 15), random.randint(0, 15))
        
        # Create a navigable path
        self.create_path(self.target)

        # Add random obstacles
        self.add_obstacles()

        self.graph_json = json.dumps({'graph': self.graph.tolist(), 'target': self.target})
        
        # Print the map with target and obstacles to the terminal
        self.print_map()

        self.timer = self.create_timer(2, self.timer_callback)

    def timer_callback(self):
        self.publisher_.publish(String(data=self.graph_json))

    def create_path(self, target):
        x, y = 0, 0  # Start position
        while (x, y) != target:
            self.graph[x, y] = 0  # Ensure path is clear
            if x < target[0]:
                x += 1
            elif y < target[1]:
                y += 1

        self.graph[target] = 2  # Mark the target

    def add_obstacles(self, obstacle_prob=0.2):
        for i in range(self.graph.shape[0]):
            for j in range(self.graph.shape[1]):
                if self.graph[i, j] == 0 and random.random() < obstacle_prob:
                    self.graph[i, j] = 1  # Add obstacle

    def print_map(self):
        map_message = "Map:\n"
        for row in self.graph:
            map_message += ' '.join(str(cell) for cell in row) + '\n'
        map_message += f"Target location: {self.target}"
        print(map_message)

def main(args=None):
    rclpy.init(args=args)
    graph_publisher = GraphPublisher()
    rclpy.spin(graph_publisher)
    graph_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
