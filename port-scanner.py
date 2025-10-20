import socket
import sys
import time
import concurrent.futures

if len(sys.argv) != 2:
    print("usages:.scripts.py [HOST]")
    sys.exit()

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    conn = s.connect_ex((ip, port))
    if conn==0:
        try:
            service = socket.getservbyport(port)
        except Exception:
            service = "unknown service"
        return (port, service)
    else:
        return None

def Scanner():
    host = sys.argv[1]
    ports = (20,21,22,23,25,53,69,80,139,137,443,445,1433,1434,3306,3389,8000,8080,8443)
    ip = socket.gethostbyname(host)

    print(f"starting scan on host {host} ({ip})")
    start_time = time.time()

    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port) for port in ports}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                open_ports.append(result)
    


    print("PORT\tSTATE\tSERVICE")
    for port, service in open_ports:
        print(f"{port}/tcp\topen\t{service}")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nScan completed in {end_time - start_time:.2f} seconds")

Scanner()
    
