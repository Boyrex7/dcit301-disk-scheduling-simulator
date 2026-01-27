def parse_requests(user_input: str) -> list[int]:
    """
    Convert a comma-separated string like "98,183,37" into a list of integers.
    Spaces are allowed: "98, 183, 37".
    """
    parts = [p.strip() for p in user_input.split(",")]
    requests = [int(p) for p in parts if p != ""]
    return requests


def validate_inputs(requests: list[int], disk_min: int, disk_max: int, head_start: int) -> None:
    """
    Validate disk configuration and request values.
    Raises ValueError if something is wrong.
    """
    if disk_min > disk_max:
        raise ValueError("disk_min cannot be greater than disk_max.")

    if not (disk_min <= head_start <= disk_max):
        raise ValueError(f"Initial head position {head_start} is outside disk range {disk_min}-{disk_max}.")

    for r in requests:
        if not (disk_min <= r <= disk_max):
            raise ValueError(f"Request {r} is outside disk range {disk_min}-{disk_max}.")


def total_head_movement(path: list[int]) -> int:
    """
    Total head movement = sum of absolute differences between consecutive head positions.
    This is proportional to seek time for HDD scheduling comparisons.
    """
    total = 0
    for i in range(len(path) - 1):
        total += abs(path[i + 1] - path[i])
    return total


def movement_bar(frm: int, to: int) -> str:
    """
    Simple ASCII visualization of head movement.
    - '>' means moving to higher cylinders
    - '<' means moving to lower cylinders
    - '-' means no movement
    """
    distance = abs(to - frm)

    # Scale distance and cap the bar length for readability
    length = min(30, max(1, distance // 5))

    if to > frm:
        return ">" * length
    elif to < frm:
        return "<" * length
    else:
        return "-"


def print_move_table(path: list[int]) -> int:
    """
    Print a compact table of head movements.
    Returns total head movement (∝ seek time).
    """
    total = 0
    # Legend for ASCII visualization (printed once per table)
    print("\nLegend: > = moving up, < = moving down, - = no movement")
    
    print("\nStep | From -> To | Distance | Movement")
    print("-----+-----------+----------+----------------")

    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        dist = abs(b - a)
        total += dist
        bar = movement_bar(a, b)
        print(f"{i+1:>4} | {a:>4} -> {b:<4} | {dist:>8} | {bar}")

    return total


def fcfs(requests: list[int], head_start: int) -> list[int]:
    """
    FCFS Disk Scheduling:
    - Serve requests exactly in the order they arrive (no reordering).
    Returns:
      - path: the sequence of head positions visited (for visualization)
    """
    # Start from the initial head position, then follow the request order
    return [head_start] + requests


def sstf(requests: list[int], head_start: int) -> list[int]:
    """
    SSTF Disk Scheduling:
    - Always serve the request closest to the current head position.
    Returns:
      - path: the sequence of head positions visited (for visualization)
    """
    pending = requests[:]  # copy so we can remove items
    current = head_start
    path = [current]

    while pending:
        best = pending[0]

        # check all pending requests and pick the closest one
        for r in pending:
            if abs(r - current) < abs(best - current):
                best = r

        path.append(best)
        current = best
        pending.remove(best)

    return path


def scan(requests: list[int], head_start: int, disk_min: int, disk_max: int, direction: str) -> list[int]:
    """
    SCAN (Elevator) Disk Scheduling:
    - Move in one direction serving requests, go to the end, reverse, and continue.
    Returns:
      - path: the sequence of head positions visited (for visualization)
    """
    left = sorted([r for r in requests if r < head_start])
    right = sorted([r for r in requests if r >= head_start])

    path = [head_start]

    if direction == "up":
        # serve all on the right side first
        path += right
        # then go to the end of the disk before coming back
        path.append(disk_max)
        path += list(reversed(left))
    else:
        # serve all on the left side first
        path += list(reversed(left))
        path.append(disk_min)
        path += right

    return path


def cscan(requests: list[int], head_start: int, disk_min: int, disk_max: int, direction: str) -> list[int]:
    """
    C-SCAN Disk Scheduling:
    - Move in one direction serving requests, go to the end, wrap to start, continue.
    Returns:
      - path: the sequence of head positions visited (for visualization)
    """
    left = sorted([r for r in requests if r < head_start])
    right = sorted([r for r in requests if r >= head_start])

    path = [head_start]

    if direction == "up":
        path += right
        # reach the end, then wrap around to the beginning
        path.append(disk_max)
        path.append(disk_min)
        path += left
    else:
        path += list(reversed(left))
        path.append(disk_min)
        path.append(disk_max)
        path += list(reversed(right))

    return path


def look(requests: list[int], head_start: int, direction: str) -> list[int]:
    """
    LOOK Disk Scheduling:
    - Like SCAN, but only goes as far as the last request in a direction (not disk end).
    Returns:
      - path: the sequence of head positions visited (for visualization)
    """
    left = sorted([r for r in requests if r < head_start])
    right = sorted([r for r in requests if r >= head_start])

    path = [head_start]

    if direction == "up":
        path += right
        # reverse at the last request (no need to go to disk end)
        path += list(reversed(left))
    else:
        path += list(reversed(left))
        path += right

    return path


def run_test_cases() -> None:
    """
    Run predefined test cases to compare the algorithms quickly.
    This helps with "Test cases and validation procedures" requirement.
    """
    test_cases = [
        {
            "name": "Test Case 1: Random requests",
            "disk_min": 0,
            "disk_max": 199,
            "head_start": 53,
            "requests": [98, 183, 37, 122, 14, 124, 65, 67],
            "direction": "up",
        },
        {
            "name": "Test Case 2: Sorted requests",
            "disk_min": 0,
            "disk_max": 199,
            "head_start": 50,
            "requests": [10, 20, 30, 40, 60, 70, 80],
            "direction": "up",
        },
        {
            "name": "Test Case 3: Reverse sorted requests",
            "disk_min": 0,
            "disk_max": 199,
            "head_start": 100,
            "requests": [180, 160, 140, 120, 60, 40, 20],
            "direction": "down",
        },
        {
            "name": "Test Case 4: Clustered requests",
            "disk_min": 0,
            "disk_max": 199,
            "head_start": 90,
            "requests": [85, 86, 87, 150, 160, 170],
            "direction": "up",
        },
    ]

    print("\n=== Running Predefined Test Cases ===")

    for case in test_cases:
        name = case["name"]
        disk_min = case["disk_min"]
        disk_max = case["disk_max"]
        head_start = case["head_start"]
        requests = case["requests"]
        direction = case["direction"]

        print("\n==============================")
        print(name)
        print(f"Disk range: {disk_min} to {disk_max}")
        print(f"Initial head position: {head_start}")
        print("Request queue:", requests)
        print("Direction:", direction)

        # Validate before running
        validate_inputs(requests, disk_min, disk_max, head_start)

        # Build results (movement only, quick compare)
        results: list[tuple[str, int]] = []
        results.append(("FCFS", total_head_movement(fcfs(requests, head_start))))
        results.append(("SSTF", total_head_movement(sstf(requests, head_start))))
        results.append(("SCAN", total_head_movement(scan(requests, head_start, disk_min, disk_max, direction))))
        results.append(("C-SCAN", total_head_movement(cscan(requests, head_start, disk_min, disk_max, direction))))
        results.append(("LOOK", total_head_movement(look(requests, head_start, direction))))

        print("\n=== Comparison Summary (Lower head movement = better performance) ===")
        results.sort(key=lambda x: x[1])
        for algo, move in results:
            print(f"{algo:6} : {move} cylinders")


def main():
    """
    Disk Scheduling Mini Simulator (CLI):
    - Takes disk config and request queue from user
    - Runs one algorithm (or all)
    - Prints path + total head movement (seek-time proportional)
    """
    print("=== Disk Scheduling Mini Simulator ===")

    # Keep running until the user says stop
    while True:
        try:
            # Disk configuration input
            disk_min = int(input("Enter minimum cylinder (e.g., 0): ").strip())
            disk_max = int(input("Enter maximum cylinder (e.g., 199): ").strip())
            head_start = int(input("Enter initial head position: ").strip())

            # Disk request queue input
            req_str = input("Enter disk requests (comma-separated): ").strip()
            requests = parse_requests(req_str)

            # Validate inputs before running algorithm
            validate_inputs(requests, disk_min, disk_max, head_start)

            # Direction input (used by SCAN / C-SCAN / LOOK)
            direction = input("Enter direction (up/down) [up]: ").strip().lower()
            if direction == "":
                direction = "up"
            if direction not in ["up", "down"]:
                print("Input error: Direction must be 'up' or 'down'. Try again.\n")
                continue

            # Show quick summary (nice for demo)
            print("\n--- Current Setup ---")
            print(f"Disk range: {disk_min} to {disk_max}")
            print(f"Initial head position: {head_start}")
            print("Request queue:", requests)

            # Choose algorithm
            print("\nChoose an algorithm:")
            print("1) FCFS  2) SSTF  3) SCAN  4) C-SCAN  5) LOOK  6) Run ALL  7) Run Test Cases  0) Exit")
            choice = input("Enter choice: ").strip()

            # Exit option
            if choice == "0":
                print("Exiting... Bye 👋")
                break

            # Small helper inside main (keeps things simple)
            def show_results(name: str, path: list[int]) -> int:
                print(f"\n--- {name} Results ---")
                print("Service path:", " -> ".join(map(str, path)))
                movement = print_move_table(path)
                print(f"Total head movement (∝ seek time): {movement} cylinders")
                return movement

            if choice == "1":
                show_results("FCFS", fcfs(requests, head_start))

            elif choice == "2":
                show_results("SSTF", sstf(requests, head_start))

            elif choice == "3":
                show_results("SCAN", scan(requests, head_start, disk_min, disk_max, direction))

            elif choice == "4":
                show_results("C-SCAN", cscan(requests, head_start, disk_min, disk_max, direction))

            elif choice == "5":
                show_results("LOOK", look(requests, head_start, direction))

            elif choice == "6":
                results: list[tuple[str, int]] = []

                results.append(("FCFS", show_results("FCFS", fcfs(requests, head_start))))
                results.append(("SSTF", show_results("SSTF", sstf(requests, head_start))))
                results.append(("SCAN", show_results("SCAN", scan(requests, head_start, disk_min, disk_max, direction))))
                results.append(("C-SCAN", show_results("C-SCAN", cscan(requests, head_start, disk_min, disk_max, direction))))
                results.append(("LOOK", show_results("LOOK", look(requests, head_start, direction))))

                # Quick comparison summary (lower movement = better performance)
                print("\n=== Comparison Summary (Lower head movement = better performance) ===")
                results.sort(key=lambda x: x[1])
                for name, move in results:
                    print(f"{name:6} : {move} cylinders")

            elif choice == "7":
                run_test_cases()

            else:
                print("Input error: Invalid choice. Pick 0-7.\n")
                continue

            # Run again prompt
            again = input("\nRun another test? (y/n) [y]: ").strip().lower()
            if again == "" or again == "y":
                print("")  # just spacing
                continue
            else:
                print("Alright, done. Bye 👋")
                break

        except ValueError as e:
            # Handle invalid user input gracefully (and keep the loop running)
            print("\nInput error:", e)
            print("Try again.\n")


if __name__ == "__main__":
    # Entry point of the program
    try:
        main()
    except ValueError as e:
        # Handle invalid user input gracefully
        print("\nInput error:", e)

