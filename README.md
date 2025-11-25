# Disk I/O Scheduling Simulator  
A Python-based simulator that evaluates the performance of common disk scheduling algorithms used in operating systems.  
This project was developed as part of the **Capstone Project – Operating Systems and Technologies (CPE 2103)** at **Soroti University**.

---

# Project Description
This simulator models how different disk I/O scheduling algorithms handle multiple disk access requests.  
Disk scheduling affects:
- Speed of data retrieval  
- System responsiveness  
- Fairness across multiple users  

This project implements and compares:
- **FCFS** – First-Come, First-Served  
- **SSTF** – Shortest Seek Time First  
- **SCAN** – Elevator Algorithm  
- **C-SCAN** – Circular SCAN  

The goal is to measure and visualize:
- Total head movement  
- Average wait time  
- Maximum wait time (starvation detection)  





# Features
- Generate random or clustered disk request queues  
- Simulation of  all four major scheduling algorithms  
- Visualize disk head movement using Matplotlib  
- Compare fairness vs throughput  
- Save graphs in the `images/` folder  
- Easy to run and extend



## Project Structure
project-folder/
│
├── disk_model.py and disksimulator.py
├── requirements.py
├── requirements.txt
├── README.md
│
└── disk images/
├── fcfs_graph.png
├── sstf_graph.png
├── scan_graph.png
└── cscan_graph.png





Clone the repository
```bash
git clone https://github.com/Isaiahpromax-hub/I-O-disk-scheduler-.git
