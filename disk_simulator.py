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


def print_move_table(path: list[int]) -> int:
    """
    Print a compact table of head movements.
    Returns total head movement (∝ seek time).
    """
    total = 0
    print("\nStep | From -> To | Distance")
    print("-----+-----------+---------")

    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        dist = abs(b - a)
        total += dist
        print(f"{i+1:>4} | {a:>4} -> {b:<4} | {dist:>8}")

    return total


# ---------------- Disk Scheduling Algorithms ----------------

def fcfs(requests: list[int], head_start: int) -> list[int]:
    """FCFS Disk Scheduling"""
    return [head_start] + requests


def sstf(requests: list[int], head_start: int) -> list[int]:
    """SSTF Disk Scheduling"""
    pending = requests[:]
    current = head_start
    path = [current]

    while pending:
        best = pending[0]
        for r in pending:
            if abs(r - current) < abs(best - current):
                best = r

        path.append(best)
        current = best
        pending.remove(best)

    return path


def scan(requests: list[int], head_start: int, disk_min: int, disk_max: int, direction: str) -> list[int]:
    """SCAN Disk Scheduling"""
    left = sorted([r for r in requests if r < head_start])
    right = sorted([r for r in requests if r >= head_start])

    path = [head_start]

    if direction == "up":
        path += right
        path.append(disk_max)
        path += list(reversed(left))
    else:
        path += list(reversed(left))
        path.append(disk_min)
        path += right

    return path


def cscan(requests: list[int], head_start: int, disk_min: int, disk_max: int, direction: str) -> list[int]:
    """C-SCAN Disk Scheduling"""
    left = sorted([r for r in requests if r < head_start])
    right = sorted([r for r in requests if r >= head_start])

    path = [head_start]

    if direction == "up":
        path += right
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
    """LOOK Disk Scheduling"""
    left = sorted([r for r in requests if r < head_start])
    right = sorted([r for r in requests if r >= head_start])

    path = [head_start]

    if direction == "up":
        path += right
        path += list(reversed(left))
    else:
        path += list(reversed(left))
        path += right

    return path


# ---------------- Test Cases ----------------

def run_test_cases():
    """
    Run predefined test cases to compare disk scheduling algorithms.
    """
    test_cases = [
        {
            "name": "Test Case 1: Random requests",
            "disk_min": 0,
            "disk_max": 199,
            "head": 53,
            "requests": [98, 183, 37, 122, 14, 124, 65, 67],
            "direction": "up",
        },
        {
            "name": "Test Case 2: Sorted requests",
            "disk_min": 0,
            "disk_max": 199,
            "head": 50,
            "requests": [10, 20, 30, 40, 60, 70, 80],
            "direction": "up",
        },
        {
            "name": "Test Case 3: Reverse sorted requests",
            "disk_min": 0,
            "disk_max": 199,
            "head": 100,
            "requests": [180, 160, 140, 120, 60, 40, 20],
            "direction": "down",
        },
        {
            "name": "Test Case 4: Clustered requests",
            "disk_min": 0,
            "disk_max": 199,
            "head": 90,
            "requests": [85, 86, 87, 150, 160, 170],
            "direction": "up",
        },
    ]

    for case in test_cases:
        print("\n==============================")
        print(case["name"])
        print("Disk range:", case["disk_min"], "-", case["disk_max"])
        print("Initial head position:", case["head"])
        print("Request queue:", case["requests"])

        validate_inputs(case["requests"], case["disk_min"], case["disk_max"], case["head"])

        results = []

        results.append(("FCFS", total_head_movement(fcfs(case["requests"], case["head"]))))
        results.append(("SSTF", total_head_movement(sstf(case["requests"], case["head"]))))
        results.append(("SCAN", total_head_movement(
            scan(case["requests"], case["head"], case["disk_min"], case["disk_max"], case["direction"])
        )))
        results.append(("C-SCAN", total_head_movement(
            cscan(case["requests"], case["head"], case["disk_min"], case["disk_max"], case["direction"])
        )))
        results.append(("LOOK", total_head_movement(
            look(case["requests"], case["head"], case["direction"])
        )))

        print("\nAlgorithm Comparison (Lower is better)")
        for name, move in sorted(results, key=lambda x: x[1]):
            print(f"{name:6} : {move} cylinders")


# ---------------- Main Program ----------------

def main():
    print("=== Disk Scheduling Mini Simulator ===")

    while True:
        try:
            disk_min = int(input("Enter minimum cylinder (e.g., 0): ").strip())
            disk_max = int(input("Enter maximum cylinder (e.g., 199): ").strip())
            head_start = int(input("Enter initial head position: ").strip())

            req_str = input("Enter disk requests (comma-separated): ").strip()
            requests = parse_requests(req_str)

            validate_inputs(requests, disk_min, disk_max, head_start)

            direction = input("Enter direction (up/down) [up]: ").strip().lower()
            if direction == "":
                direction = "up"
            if direction not in ["up", "down"]:
                print("Input error: Direction must be 'up' or 'down'.\n")
                continue

            print("\nChoose an algorithm:")
            print("1) FCFS  2) SSTF  3) SCAN  4) C-SCAN  5) LOOK  6) Run ALL  7) Run Test Cases  0) Exit")
            choice = input("Enter choice: ").strip()

            if choice == "0":
                break

            def show_results(name: str, path: list[int]):
                print(f"\n--- {name} Results ---")
                print("Service path:", " -> ".join(map(str, path)))
                movement = print_move_table(path)
                print(f"Total head movement (∝ seek time): {movement} cylinders")

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
                show_results("FCFS", fcfs(requests, head_start))
                show_results("SSTF", sstf(requests, head_start))
                show_results("SCAN", scan(requests, head_start, disk_min, disk_max, direction))
                show_results("C-SCAN", cscan(requests, head_start, disk_min, disk_max, direction))
                show_results("LOOK", look(requests, head_start, direction))
            elif choice == "7":
                run_test_cases()
            else:
                print("Invalid choice.\n")

            again = input("\nRun another test? (y/n) [y]: ").strip().lower()
            if again not in ["", "y"]:
                break

        except ValueError as e:
            print("\nInput error:", e)
            print("Try again.\n")


if __name__ == "__main__":
    main()


