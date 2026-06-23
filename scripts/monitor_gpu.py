import argparse
import csv
import signal
import subprocess
import time
from pathlib import Path

running = True

def stop_handler(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, stop_handler)
signal.signal(signal.SIGTERM, stop_handler)

parser = argparse.ArgumentParser()
parser.add_argument("--interval", type=float, default=1.0)
parser.add_argument("--csv", type=str, default="results/gpu_usage.csv")
parser.add_argument("--summary", type=str, default="results/gpu_summary.txt")
args = parser.parse_args()

csv_path = Path(args.csv)
summary_path = Path(args.summary)
csv_path.parent.mkdir(parents=True, exist_ok=True)
summary_path.parent.mkdir(parents=True, exist_ok=True)

cmd = [
    "nvidia-smi",
    "--query-gpu=timestamp,index,name,memory.used,memory.total,utilization.gpu",
    "--format=csv,noheader,nounits"
]

peak_mem = 0
peak_util = 0
gpu_name = ""
mem_total = 0

with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "local_time",
        "gpu_index",
        "gpu_name",
        "memory_used_mb",
        "memory_total_mb",
        "gpu_util_percent"
    ])

    print(f"[GPU Monitor] Writing to {csv_path}")
    print("[GPU Monitor] Press Ctrl+C or kill process to stop.")

    while running:
        try:
            output = subprocess.check_output(cmd, text=True)
            rows = list(csv.reader(output.splitlines()))

            for row in rows:
                timestamp = row[0].strip()
                index = row[1].strip()
                name = row[2].strip()
                memory_used = int(row[3].strip())
                memory_total = int(row[4].strip())
                gpu_util = int(row[5].strip())

                gpu_name = name
                mem_total = memory_total
                peak_mem = max(peak_mem, memory_used)
                peak_util = max(peak_util, gpu_util)

                writer.writerow([
                    timestamp,
                    index,
                    name,
                    memory_used,
                    memory_total,
                    gpu_util
                ])
                f.flush()

        except Exception as e:
            print("[GPU Monitor Error]", e)

        time.sleep(args.interval)

summary = (
    f"gpu_name: {gpu_name}\n"
    f"peak_memory_used_mb: {peak_mem}\n"
    f"memory_total_mb: {mem_total}\n"
    f"peak_gpu_utilization_percent: {peak_util}\n"
    f"csv_file: {csv_path}\n"
)

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)

print("[GPU Monitor] Summary:")
print(summary)
