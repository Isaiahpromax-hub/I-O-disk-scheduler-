# sstf_starvation_workload.py
# Compare Disk Scheduling Algorithms & Illustrate SSTF Starvation

class Disk:
    def __init__(self, total_cylinders, start_head, request_queue):
        self.total_cylinders = total_cylinders
        self.current_head = start_head
        self.request_queue = request_queue.copy()
        self.original_requests = request_queue.copy()

    def fcfs_schedule(self):
        current_head = self.current_head
        requests = self.request_queue.copy()
        total_movement = 0
        sequence = []

        for request in requests:
            total_movement += abs(current_head - request)
            sequence.append(request)
            current_head = request

        return total_movement, sequence

    def sstf_schedule(self):
        current_head = self.current_head
        requests = self.request_queue.copy()
        total_movement = 0
        sequence = []

        while requests:
            closest = min(requests, key=lambda x: abs(x - current_head))
            total_movement += abs(current_head - closest)
            sequence.append(closest)
            current_head = closest
            requests.remove(closest)

        return total_movement, sequence

    def scan_schedule(self, direction='right'):
        current_head = self.current_head
        requests = sorted(self.request_queue)
        total_movement = 0
        sequence = []
        if direction == 'right':
            right = [r for r in requests if r >= current_head]
            left = [r for r in requests if r < current_head][::-1]
            for r in right + left:
                total_movement += abs(current_head - r)
                sequence.append(r)
                current_head = r
        else:
            left = [r for r in requests if r <= current_head][::-1]
            right = [r for r in requests if r > current_head]
            for r in left + right:
                total_movement += abs(current_head - r)
                sequence.append(r)
                current_head = r
        return total_movement, sequence

    def c_scan_schedule(self, direction='right'):
        current_head = self.current_head
        requests = sorted(self.request_queue)
        total_movement = 0
        sequence = []

        if direction == 'right':
            right = [r for r in requests if r >= current_head]
            left = [r for r in requests if r < current_head]
            for r in right:
                total_movement += abs(current_head - r)
                sequence.append(r)
                current_head = r
            if left:
                # Jump to start
                total_movement += abs(current_head - (self.total_cylinders - 1))
                current_head = 0
                for r in left:
                    total_movement += abs(current_head - r)
                    sequence.append(r)
                    current_head = r
        return total_movement, sequence

if __name__ == '__main__':
    # Starvation Workload: many close requests, one far-away request
    total_cylinders = 200
    start_head = 50
    request_queue = [51, 49, 52, 48, 50, 195, 5]  # SSTF may delay 195 or 5

    disk = Disk(total_cylinders, start_head, request_queue)

    print("=== Disk Scheduling Workload Comparison ===")
    print(f"Initial Head: {disk.current_head}")
    print(f"Request Queue: {disk.request_queue}\n")

    fcfs_movement, fcfs_seq = disk.fcfs_schedule()
    sstf_movement, sstf_seq = disk.sstf_schedule()
    scan_movement, scan_seq = disk.scan_schedule(direction='right')
    cscan_movement, cscan_seq = disk.c_scan_schedule(direction='right')

    print(f"FCFS: Total Movement={fcfs_movement}, Sequence={fcfs_seq}")
    print(f"SSTF: Total Movement={sstf_movement}, Sequence={sstf_seq}  # Starvation visible")
    print(f"SCAN: Total Movement={scan_movement}, Sequence={scan_seq}")
    print(f"C-SCAN: Total Movement={cscan_movement}, Sequence={cscan_seq}")
