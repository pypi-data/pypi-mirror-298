"""Module for measuring system resources during program execution."""

import time
import subprocess
import sys
import os
import psutil


def measure_resources(script_to_measure, *script_args):
    """Measure the resources used by a script."""
    start = {"time": time.time(), "memory": psutil.Process().memory_info().rss}

    # Get the path to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, script_to_measure)

    # Start the script as a subprocess
    process = subprocess.Popen([sys.executable, script_path] + list(script_args))

    # Get the Process object for resource monitoring
    p = psutil.Process(process.pid)

    cpu_percent = []
    memory_percent = []
    try:
        io_counters_start = p.io_counters()
    except psutil.NoSuchProcess:
        io_counters_start = None

    while process.poll() is None:
        try:
            cpu_percent.append(p.cpu_percent(interval=1))
            memory_percent.append(p.memory_percent())
        except psutil.NoSuchProcess:
            break

    end = {"time": time.time(), "memory": psutil.Process().memory_info().rss}

    try:
        io_counters_end = p.io_counters()
    except psutil.NoSuchProcess:
        io_counters_end = None

    # Calculate average CPU and memory usage
    avg_cpu = sum(cpu_percent) / len(cpu_percent) if cpu_percent else 0
    avg_memory = sum(memory_percent) / len(memory_percent) if memory_percent else 0

    # Print results
    print(f"Execution time: {end['time'] - start['time']:.2f} seconds")
    print(f"Average CPU usage: {avg_cpu:.2f}%")
    print(f"Average memory usage: {avg_memory:.2f}%")
    print(
        f"Peak memory usage: {(end['memory'] - start['memory']) / (1024 * 1024):.2f} MB"
    )

    if io_counters_start and io_counters_end:
        io_read = io_counters_end.read_bytes - io_counters_start.read_bytes
        io_write = io_counters_end.write_bytes - io_counters_start.write_bytes
        print(f"Total I/O read: {io_read / (1024 * 1024):.2f} MB")
        print(f"Total I/O write: {io_write / (1024 * 1024):.2f} MB")
    else:
        print("I/O operations: Unable to measure (process ended too quickly)")


def cli():
    """Handle command-line interface for the measure_resources script."""
    if len(sys.argv) < 2:
        print("Usage: measure_resources <script_name> [args...]")
        sys.exit(1)

    script_name = sys.argv[1]
    args = sys.argv[2:]
    measure_resources(script_name, *args)


if __name__ == "__main__":
    cli()
