import tkinter as tk
from tkinter import ttk, messagebox
import disk_simulator as ds

class DiskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Simulator (Group 13)")
        self.root.geometry("900x700")

        # --- Styling ---
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass  # Fallback to default if clam is not available

        bg_color = "#f5f5f5"
        self.root.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 10))
        style.configure("TLabelFrame", background=bg_color, font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#333")
        
        # Accent Button Style
        style.configure("Accent.TButton", foreground="white", background="#0078d7", font=("Segoe UI", 9, "bold"))
        style.map("Accent.TButton", background=[("active", "#005a9e")])

        # Main Container
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Header
        ttk.Label(main_frame, text="Disk Scheduling Simulator", style="Header.TLabel").pack(pady=(0, 20))

        # --- Input Section ---
        input_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=15)
        input_frame.pack(fill="x", pady=(0, 15))

        # Row 0: Disk Range and Head
        ttk.Label(input_frame, text="Min Cylinder:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.min_cyl_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.min_cyl_var, width=10).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Max Cylinder:").grid(row=0, column=2, padx=(20, 5), pady=5, sticky="w")
        self.max_cyl_var = tk.StringVar(value="199")
        ttk.Entry(input_frame, textvariable=self.max_cyl_var, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Initial Head:").grid(row=0, column=4, padx=(20, 5), pady=5, sticky="w")
        self.head_var = tk.StringVar(value="53")
        ttk.Entry(input_frame, textvariable=self.head_var, width=10).grid(row=0, column=5, padx=5, pady=5)

        # Row 1: Requests and Direction
        ttk.Label(input_frame, text="Requests (comma-sep):").grid(row=1, column=0, padx=5, pady=15, sticky="w")
        self.req_var = tk.StringVar(value="98, 183, 37, 122, 14, 124, 65, 67")
        ttk.Entry(input_frame, textvariable=self.req_var, width=50).grid(row=1, column=1, columnspan=3, padx=5, pady=15, sticky="ew")

        ttk.Label(input_frame, text="Direction:").grid(row=1, column=4, padx=(20, 5), pady=15, sticky="w")
        self.dir_var = tk.StringVar(value="up")
        ttk.Combobox(input_frame, textvariable=self.dir_var, values=["up", "down"], state="readonly", width=8).grid(row=1, column=5, padx=5, pady=15)

        # --- Buttons Section ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(0, 15))

        # Algorithm Buttons
        algo_frame = ttk.LabelFrame(btn_frame, text="Algorithms", padding=10)
        algo_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        for algo in ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK"]:
            ttk.Button(algo_frame, text=algo, command=lambda a=algo: self.run_single(a)).pack(side="left", padx=5, fill="x", expand=True)

        # Action Buttons
        action_frame = ttk.Frame(btn_frame)
        action_frame.pack(side="right")
        
        ttk.Button(action_frame, text="Compare All", style="Accent.TButton", command=self.run_comparison).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Clear", command=self.clear_output).pack(side="left", padx=5)

        # --- Output Section ---
        output_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        output_frame.pack(fill="both", expand=True)

        self.output_text = tk.Text(output_frame, height=15, font=("Consolas", 10), state="normal", wrap="none", padx=10, pady=10)
        self.output_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text['yscrollcommand'] = scrollbar.set

        # Configure text tags for styling
        self.output_text.tag_configure("title", foreground="#0078d7", font=("Consolas", 11, "bold"))
        self.output_text.tag_configure("bold", font=("Consolas", 10, "bold"))
        self.output_text.tag_configure("header", background="#e1e1e1", font=("Consolas", 10, "bold"))

    def get_inputs(self):
        try:
            disk_min = int(self.min_cyl_var.get())
            disk_max = int(self.max_cyl_var.get())
            head_start = int(self.head_var.get())
            requests = ds.parse_requests(self.req_var.get())
            direction = self.dir_var.get()
            
            ds.validate_inputs(requests, disk_min, disk_max, head_start)
            return disk_min, disk_max, head_start, requests, direction
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def run_single(self, algo):
        data = self.get_inputs()
        if not data: return
        disk_min, disk_max, head_start, requests, direction = data

        path = []
        if algo == "FCFS": path = ds.fcfs(requests, head_start)
        elif algo == "SSTF": path = ds.sstf(requests, head_start)
        elif algo == "SCAN": path = ds.scan(requests, head_start, disk_min, disk_max, direction)
        elif algo == "C-SCAN": path = ds.cscan(requests, head_start, disk_min, disk_max, direction)
        elif algo == "LOOK": path = ds.look(requests, head_start, direction)

        total = ds.total_head_movement(path)
        
        self.output_text.insert(tk.END, f"\n=== {algo} Results ===\n", "title")
        self.output_text.insert(tk.END, f"Total Head Movement: {total} cylinders\n\n", "bold")
        self.output_text.insert(tk.END, "Step | From -> To   | Distance\n", "header")
        self.output_text.insert(tk.END, "-----|--------------|---------\n", "header")
        
        for i in range(len(path) - 1):
            dist = abs(path[i+1] - path[i])
            self.output_text.insert(tk.END, f"{i+1:>4} | {path[i]:>4} -> {path[i+1]:<4} | {dist:>8}\n")
        self.output_text.see(tk.END)

    def run_comparison(self):
        data = self.get_inputs()
        if not data: return
        disk_min, disk_max, head_start, requests, direction = data

        results = []
        results.append(("FCFS", ds.total_head_movement(ds.fcfs(requests, head_start))))
        results.append(("SSTF", ds.total_head_movement(ds.sstf(requests, head_start))))
        results.append(("SCAN", ds.total_head_movement(ds.scan(requests, head_start, disk_min, disk_max, direction))))
        results.append(("C-SCAN", ds.total_head_movement(ds.cscan(requests, head_start, disk_min, disk_max, direction))))
        results.append(("LOOK", ds.total_head_movement(ds.look(requests, head_start, direction))))

        results.sort(key=lambda x: x[1])

        self.output_text.insert(tk.END, "\n=== Algorithm Comparison ===\n", "title")
        self.output_text.insert(tk.END, "(Sorted by efficiency)\n\n", "bold")
        for name, move in results:
            self.output_text.insert(tk.END, f"{name:6} : {move} cylinders\n")
        self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulerGUI(root)
    root.mainloop()