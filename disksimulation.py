# ==============================================
# Disk I/O Scheduling Simulator - Disk Model
# Complete Implementation with All Algorithms
# FCFS, SSTF, SCAN, C-SCAN Scheduling Algorithms
# ==============================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

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
        self.request_queue = request_queue.copy()
        self.original_requests = request_queue.copy()

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
            marker = "↑" if i <= self.current_head < i + 25 else "-"
            print(f"{i:3d} {marker}")
        print(f"\nCurrent Head: {self.current_head}")
        print(f"Requests: {self.request_queue}\n")

    def fcfs_schedule(self):
        """
        Implement FCFS (First-Come-First-Serve) disk scheduling algorithm.
        Processes requests in the order they were received.
        """
        print("\n" + "="*50)
        print("FCFS DISK SCHEDULING ALGORITHM")
        print("="*50)
        
        current_head = self.current_head
        requests = self.request_queue.copy()
        
        total_movement = 0
        sequence = []
        movements = []
        
        print(f"Starting head position: {current_head}")
        print(f"Request queue: {requests}")
        print("\nProcessing requests in FCFS order:")
        print("-" * 40)
        
        for i, request in enumerate(requests):
            movement = abs(current_head - request)
            total_movement += movement
            sequence.append(request)
            movements.append(movement)
            
            print(f"Step {i+1}: Head {current_head:3d} → Request {request:3d} "
                  f"| Movement: {movement:3d} cylinders")
            current_head = request
        
        average_seek = total_movement / len(requests) if requests else 0
        
        print("-" * 40)
        print(f"Total Head Movement: {total_movement} cylinders")
        print(f"Average Seek Time: {average_seek:.2f} cylinders per request")
        print(f"Final Head Position: {current_head}")
        
        return {
            'algorithm': 'FCFS',
            'total_movement': total_movement,
            'average_seek': average_seek,
            'sequence': sequence,
            'movements': movements,
            'final_position': current_head
        }

    def sstf_schedule(self):
        """
        Implement SSTF (Shortest Seek Time First) disk scheduling algorithm.
        Always services the closest request to the current head position.
        """
        print("\n" + "="*50)
        print("SSTF DISK SCHEDULING ALGORITHM")
        print("="*50)
        
        current_head = self.current_head
        requests = self.request_queue.copy()
        
        total_movement = 0
        sequence = []
        movements = []
        
        print(f"Starting head position: {current_head}")
        print(f"Request queue: {requests}")
        print("\nProcessing requests using SSTF:")
        print("-" * 40)
        
        step = 1
        while requests:
            # Find the closest request
            closest_request = min(requests, key=lambda x: abs(x - current_head))
            movement = abs(current_head - closest_request)
            total_movement += movement
            
            sequence.append(closest_request)
            movements.append(movement)
            
            print(f"Step {step}: Head {current_head:3d} → Request {closest_request:3d} "
                  f"| Movement: {movement:3d} cylinders")
            
            current_head = closest_request
            requests.remove(closest_request)
            step += 1
        
        average_seek = total_movement / len(self.request_queue) if self.request_queue else 0
        
        print("-" * 40)
        print(f"Total Head Movement: {total_movement} cylinders")
        print(f"Average Seek Time: {average_seek:.2f} cylinders per request")
        print(f"Final Head Position: {current_head}")
        
        return {
            'algorithm': 'SSTF',
            'total_movement': total_movement,
            'average_seek': average_seek,
            'sequence': sequence,
            'movements': movements,
            'final_position': current_head
        }

    def scan_schedule(self, direction='right'):
        """
        Implement SCAN (Elevator) disk scheduling algorithm.
        The disk arm moves in one direction, servicing requests until it reaches
        the end, then reverses direction.
        :param direction: Initial direction ('right' or 'left')
        """
        print("\n" + "="*50)
        print("SCAN DISK SCHEDULING ALGORITHM")
        print("="*50)
        
        current_head = self.current_head
        requests = self.request_queue.copy()
        
        total_movement = 0
        sequence = []
        movements = []
        
        print(f"Starting head position: {current_head}")
        print(f"Initial direction: {direction}")
        print(f"Request queue: {requests}")
        print("\nProcessing requests using SCAN:")
        print("-" * 40)
        
        step = 1
        current_direction = direction
        
        while requests:
            if current_direction == 'right':
                # Find requests in the right direction
                right_requests = [r for r in requests if r >= current_head]
                if right_requests:
                    next_request = min(right_requests)
                    movement = abs(current_head - next_request)
                    total_movement += movement
                    sequence.append(next_request)
                    movements.append(movement)
                    
                    print(f"Step {step}: Head {current_head:3d} → Request {next_request:3d} "
                          f"| Movement: {movement:3d} cylinders | Direction: {current_direction}")
                    
                    current_head = next_request
                    requests.remove(next_request)
                    step += 1
                else:
                    # No more requests to the right, go to end and reverse
                    movement = abs(current_head - (self.total_cylinders - 1))
                    total_movement += movement
                    sequence.append(self.total_cylinders - 1)
                    movements.append(movement)
                    
                    print(f"Step {step}: Head {current_head:3d} → End {self.total_cylinders - 1:3d} "
                          f"| Movement: {movement:3d} cylinders | Changing direction to LEFT")
                    
                    current_head = self.total_cylinders - 1
                    current_direction = 'left'
                    step += 1
            else:  # direction == 'left'
                # Find requests in the left direction
                left_requests = [r for r in requests if r <= current_head]
                if left_requests:
                    next_request = max(left_requests)
                    movement = abs(current_head - next_request)
                    total_movement += movement
                    sequence.append(next_request)
                    movements.append(movement)
                    
                    print(f"Step {step}: Head {current_head:3d} → Request {next_request:3d} "
                          f"| Movement: {movement:3d} cylinders | Direction: {current_direction}")
                    
                    current_head = next_request
                    requests.remove(next_request)
                    step += 1
                else:
                    # No more requests to the left, go to start and reverse
                    movement = abs(current_head - 0)
                    total_movement += movement
                    sequence.append(0)
                    movements.append(movement)
                    
                    print(f"Step {step}: Head {current_head:3d} → Start {0:3d} "
                          f"| Movement: {movement:3d} cylinders | Changing direction to RIGHT")
                    
                    current_head = 0
                    current_direction = 'right'
                    step += 1
        
        average_seek = total_movement / len(self.request_queue) if self.request_queue else 0
        
        print("-" * 40)
        print(f"Total Head Movement: {total_movement} cylinders")
        print(f"Average Seek Time: {average_seek:.2f} cylinders per request")
        print(f"Final Head Position: {current_head}")
        
        return {
            'algorithm': 'SCAN',
            'total_movement': total_movement,
            'average_seek': average_seek,
            'sequence': sequence,
            'movements': movements,
            'final_position': current_head,
            'direction': direction
        }

    def c_scan_schedule(self, direction='right'):
        """
        Implement C-SCAN (Circular SCAN) disk scheduling algorithm.
        The disk arm moves in one direction, servicing requests until it reaches
        the end, then jumps to the opposite end and continues.
        :param direction: Initial direction ('right' or 'left')
        """
        print("\n" + "="*50)
        print("C-SCAN DISK SCHEDULING ALGORITHM")
        print("="*50)
        
        current_head = self.current_head
        requests = self.request_queue.copy()
        
        total_movement = 0
        sequence = []
        movements = []
        
        print(f"Starting head position: {current_head}")
        print(f"Initial direction: {direction}")
        print(f"Request queue: {requests}")
        print("\nProcessing requests using C-SCAN:")
        print("-" * 40)
        
        step = 1
        current_direction = direction
        
        while requests:
            if current_direction == 'right':
                # Find requests in the right direction
                right_requests = [r for r in requests if r >= current_head]
                if right_requests:
                    next_request = min(right_requests)
                    movement = abs(current_head - next_request)
                    total_movement += movement
                    sequence.append(next_request)
                    movements.append(movement)
                    
                    print(f"Step {step}: Head {current_head:3d} → Request {next_request:3d} "
                          f"| Movement: {movement:3d} cylinders | Direction: {current_direction}")
                    
                    current_head = next_request
                    requests.remove(next_request)
                    step += 1
                else:
                    # No more requests to the right, jump to start
                    movement_to_end = abs(current_head - (self.total_cylinders - 1))
                    total_movement += movement_to_end
                    
                    sequence.append(self.total_cylinders - 1)
                    movements.append(movement_to_end)
                    
                    print(f"Step {step}: Head {current_head:3d} → End {self.total_cylinders - 1:3d} "
                          f"| Movement: {movement_to_end:3d} cylinders")
                    
                    # Jump to start (movement counted)
                    jump_movement = self.total_cylinders - 1
                    total_movement += jump_movement
                    
                    step += 1
                    print(f"Step {step}: Jump from {self.total_cylinders - 1:3d} → Start {0:3d} "
                          f"| Movement: {jump_movement:3d} cylinders")
                    
                    current_head = 0
                    step += 1
            else:  # direction == 'left'
                # Find requests in the left direction
                left_requests = [r for r in requests if r <= current_head]
                if left_requests:
                    next_request = max(left_requests)
                    movement = abs(current_head - next_request)
                    total_movement += movement
                    sequence.append(next_request)
                    movements.append(movement)
                    
                    print(f"Step {step}: Head {current_head:3d} → Request {next_request:3d} "
                          f"| Movement: {movement:3d} cylinders | Direction: {current_direction}")
                    
                    current_head = next_request
                    requests.remove(next_request)
                    step += 1
                else:
                    # No more requests to the left, jump to end
                    movement_to_start = abs(current_head - 0)
                    total_movement += movement_to_start
                    
                    sequence.append(0)
                    movements.append(movement_to_start)
                    
                    print(f"Step {step}: Head {current_head:3d} → Start {0:3d} "
                          f"| Movement: {movement_to_start:3d} cylinders")
                    
                    # Jump to end (movement counted)
                    jump_movement = self.total_cylinders - 1
                    total_movement += jump_movement
                    
                    step += 1
                    print(f"Step {step}: Jump from {0:3d} → End {self.total_cylinders - 1:3d} "
                          f"| Movement: {jump_movement:3d} cylinders")
                    
                    current_head = self.total_cylinders - 1
                    step += 1
        
        average_seek = total_movement / len(self.request_queue) if self.request_queue else 0
        
        print("-" * 40)
        print(f"Total Head Movement: {total_movement} cylinders")
        print(f"Average Seek Time: {average_seek:.2f} cylinders per request")
        print(f"Final Head Position: {current_head}")
        
        return {
            'algorithm': 'C-SCAN',
            'total_movement': total_movement,
            'average_seek': average_seek,
            'sequence': sequence,
            'movements': movements,
            'final_position': current_head,
            'direction': direction
        }

    def plot_algorithm_comparison(self, results_dict):
        """
        Create a comparison visualization of all algorithms' head movements.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        algorithms = list(results_dict.keys())
        
        for idx, algo_name in enumerate(algorithms):
            if algo_name in results_dict:
                results = results_dict[algo_name]
                # Create the sequence including starting position
                full_sequence = [self.current_head] + results['sequence']
                
                ax = axes[idx]
                ax.plot(range(len(full_sequence)), full_sequence, 'bo-', 
                       linewidth=2, markersize=6, label='Head Movement Path')
                
                # Highlight positions
                ax.plot(0, full_sequence[0], 'go', markersize=8, 
                       label=f'Start: {full_sequence[0]}')
                ax.plot(len(full_sequence)-1, full_sequence[-1], 'ro', markersize=8, 
                       label=f'End: {full_sequence[-1]}')
                
                ax.set_xlabel('Step Number')
                ax.set_ylabel('Cylinder Number')
                ax.set_title(f'{algo_name} - Total Movement: {results["total_movement"]}')
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Add annotations for key points
                for i, cyl in enumerate(full_sequence):
                    if i == 0 or i == len(full_sequence)-1 or i % 2 == 0:
                        ax.annotate(f'{cyl}', (i, cyl), textcoords="offset points", 
                                  xytext=(0,8), ha='center', fontsize=8)
        
        plt.tight_layout()
        plt.show()

    def display_comprehensive_comparison(self, all_results):
        """
        Display a comprehensive comparison table of all algorithms.
        """
        table_data = []
        
        # Add header
        table_data.append(["Algorithm", "Total Movement", "Average Seek", 
                          "Final Position", "Efficiency"])
        table_data.append(["-" * 12, "-" * 15, "-" * 12, "-" * 15, "-" * 12])
        
        # Find the algorithm with minimum movement for efficiency comparison
        min_movement = min(result['total_movement'] for result in all_results.values())
        
        for algo_name, results in all_results.items():
            efficiency = (min_movement / results['total_movement']) * 100
            table_data.append([
                algo_name,
                results['total_movement'],
                f"{results['average_seek']:.2f}",
                results['final_position'],
                f"{efficiency:.1f}%"
            ])
        
        print("\n" + "="*70)
        print("COMPREHENSIVE ALGORITHM COMPARISON")
        print("="*70)
        print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
        
        # Additional comparison metrics
        print(f"\nInitial Head Position: {self.current_head}")
        print(f"Request Queue: {self.original_requests}")
        print(f"Total Cylinders: {self.total_cylinders}")
        
        # Best algorithm recommendation
        best_algo = min(all_results.items(), key=lambda x: x[1]['total_movement'])
        print(f"\n⭐ BEST ALGORITHM: {best_algo[0]} "
              f"(Total Movement: {best_algo[1]['total_movement']} cylinders)")

# Example usage with all scheduling algorithms
if __name__ == '__main__':
    # Initialize disk parameters
    total_cylinders = 200
    current_head = 50
    request_queue = [82, 170, 43, 140, 24, 16, 190]

    # Create a Disk object
    disk = Disk(total_cylinders, current_head, request_queue)

    # Display disk info
    disk.display_info()
    disk.visualize_disk()

    # Run all scheduling algorithms and collect results
    all_results = {}

    print("\n" + "="*80)
    print("RUNNING ALL DISK SCHEDULING ALGORITHMS")
    print("="*80)

    # FCFS Scheduling
    print("\n>>> Running FCFS Algorithm...")
    fcfs_results = disk.fcfs_schedule()
    all_results['FCFS'] = fcfs_results

    # SSTF Scheduling
    print("\n>>> Running SSTF Algorithm...")
    sstf_results = disk.sstf_schedule()
    all_results['SSTF'] = sstf_results

    # SCAN Scheduling
    print("\n>>> Running SCAN Algorithm...")
    scan_results = disk.scan_schedule(direction='right')
    all_results['SCAN'] = scan_results

    # C-SCAN Scheduling
    print("\n>>> Running C-SCAN Algorithm...")
    c_scan_results = disk.c_scan_schedule(direction='right')
    all_results['C-SCAN'] = c_scan_results

    # Display comprehensive comparison
    disk.display_comprehensive_comparison(all_results)

    # Plot comparison of all algorithms
    print("\n>>> Generating comparison plots...")
    disk.plot_algorithm_comparison(all_results)

    print("\n" + "="*80)
    print("ALL ALGORITHMS EXECUTED SUCCESSFULLY!")
    print("="*80)