import socket
import threading
import argparse
from queue import Queue

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        print(f"Port {port} is open")
    sock.close()

def worker(target, ports):
    while not ports.empty():
        port = ports.get()
        scan_port(target, port)
        ports.task_done()

def scan_ports(target, start_port, end_port, num_threads):
    print(f"Scanning ports on {target}...\n")
    
    ports = Queue()

    for port in range(start_port, end_port + 1):
        ports.put(port)

    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(target, ports))
        thread.daemon = True
        thread.start()

    ports.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Starting port")
    parser.add_argument("end_port", type=int, help="Ending port")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (default: 5)")

    args = parser.parse_args()

    scan_ports(args.target, args.start_port, args.end_port, args.threads)
