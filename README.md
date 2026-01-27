# Disk Scheduling Algorithm Simulator (DCIT301)

This project is a **Disk Scheduling Algorithm Simulator** developed as part of the  
**DCIT301 – Operating Systems** course at the **University of Ghana**.

The simulator implements and compares classical disk scheduling algorithms with the objective of **minimizing disk head movement and improving seek time performance**.

---

## Implemented Algorithms

The simulator supports the following disk scheduling algorithms:

- **First Come First Serve (FCFS)**
- **Shortest Seek Time First (SSTF)**
- **SCAN (Elevator Algorithm)**
- **C-SCAN (Circular SCAN)**
- **LOOK**

Each algorithm services disk requests differently, leading to variations in performance, fairness, and total head movement.

---

## Features

- Command Line Interface (CLI)
- Accepts disk request queues as input
- Supports different disk configurations:
  - Minimum cylinder
  - Maximum cylinder
  - Initial disk head position
- Calculates:
  - Disk head movement
  - Seek time (proportional to total head movement)
- Step-by-step text-based visualization of disk head movement
- Automated test cases for algorithm comparison
- Input validation to prevent invalid configurations

---

## Testing and Evaluation

The simulator includes predefined test cases representing different disk request patterns, such as:

- Random requests
- Sorted requests
- Reverse sorted requests
- Clustered requests

Each test case runs all algorithms and compares their **total head movement**.
Lower total head movement indicates better performance since seek time is proportional to head movement.

Testing and validation files are located in the `testing/` directory.


## How to Run the Simulator

Ensure **Python 3** is installed, then run the following command:

```bash
python disk_simulator.py
