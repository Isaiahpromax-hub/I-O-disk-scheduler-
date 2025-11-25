
# Disk I/O Scheduling Simulator - Disk Model
# Week 1: Research & Modeling


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

# 1. Define the Disk class to represent the disk geometry
class Disk:
    def __init__(self, total_cylinders, start_head, request_queue):
        """
        Initialize the Disk model.
        :param total_cylinders: Total number of cylinders (e.g., 200)
        :param start_head: Initial position of the disk head
        :param request_queue: List of cylinder requests
        """
        self.total_cylinders = total_cylinders
        self.current_head = start_head
        self.request_queue = request_queue

    def display_info(self):
        """Display basic disk information."""
        print("=== Disk Geometry & I/O Requests ===")
        print(f"Total Cylinders: {self.total_cylinders}")
        print(f"Current Head Position: {self.current_head}")
        print(f"Pending Requests: {self.request_queue}")
        print("===================================")

    def visualize_disk(self):
        """Display a simple text-based visualization of the disk."""
        print("\nDisk Cylinder Layout (Simplified View):")
        for i in range(0, self.total_cylinders, 25):
            marker = "↑" if i == self.current_head else "-"
            print(f"{i:3d} {marker}")

        print(f"\nCurrent Head: {self.current_head}")
        print(f"Requests: {self.request_queue}\n")




# 2. Example 
if __name__ == "__main__":
    # Initialize disk parameters
    total_cylinders = 200
    current_head = 50
    request_queue = [82, 170, 43, 140, 24, 16, 190]

    # Create a Disk object
    disk = Disk(total_cylinders, current_head, request_queue)

    # Display disk info
    disk.display_info()

    # Show a simple visualization
    disk.visualize_disk()
