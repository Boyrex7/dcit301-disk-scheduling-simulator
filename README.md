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

---

## How to Run the Simulator

Ensure **Python 3** is installed, then run the following command:

```bash
python disk_simulator.py 

Follow the on-screen prompts to:

1. Enter disk configuration details

2. Provide a disk request queue

3. Select a disk scheduling algorithm

4. View disk head movement and performance results
```

---

## Course Information

Course: **DCIT301 – Operating Systems**

Institution: **University of Ghana**

Group: Group 13

---

## References

Disk scheduling concepts and algorithms are based on standard Operating Systems literature, including the course textbook (Operating System Concepts by Abraham Silberschatz, Peter Baer Galvin and Greg Gagne)


=====================================================================
## How to Run the GUI

1.  **Create a virtual environment:**
    ```bash
    python -m venv env
    ```

2.  **Activate the virtual environment:**

    *   **On Windows (PowerShell):**
        ```powershell
        .\env\Scripts\Activate.ps1
        ```
        > **Note:** If you encounter an error, you may need to set the execution policy by running this command in PowerShell:
        > `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

    *   **On Windows (Command Prompt):**
        ```cmd
        env\Scripts\activate.bat
        ```

    *   **On macOS and Linux:**
        ```bash
        source env/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the GUI application:**
    ```bash
    python disk_simulator_gui.py


  
5.  **GROUP MEMBERS:**
    ```BASH
    
            | ID        | Name                                 | Roles             |
            |-----------|--------------------------------------|-------------------|
            | 22039152  | Asante Opuni Frimpong                | ----------------  |
            | 22038956  | Mubarak Iddris                       | ----------------  |
            | 22223762  | Ashley Rexford Seth                  | ----------------  |
            | 22019132  | Felicity Dzidzorli Zanu-Tsikata      | ----------------  |
            | 22245133  | Donbeinaa Juliana Dome-im            | ----------------  |
            | 22169253  | Ansah Larbi Edward Junior            | ----------------  |
            | 22019894  | Fransis Akyeaw Amposah               | ----------------  |