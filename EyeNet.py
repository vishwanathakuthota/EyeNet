import argparse
import time
from icmplib import ping
from scapy.all import arping
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

def scan_network(target_ip):
    """Continuously scan a network and display active IPs in a table."""
    print(f"Starting continuous scan on {target_ip}...")
    active_hosts = {}
    
    while True:
        ans, _ = arping(target_ip, verbose=0)
        current_time = time.time()
        
        for sent, received in ans:
            ip = received.psrc
            if ip not in active_hosts:
                active_hosts[ip] = {'active_since': current_time, 'last_seen': current_time}
            else:
                active_hosts[ip]['last_seen'] = current_time
        
        # Display table
        table = Table(title="Network Monitoring", show_lines=True)
        table.add_column("IP Address", justify="center")
        table.add_column("MAC Address", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Active Duration (s)", justify="center")
        
        for ip, data in list(active_hosts.items()):
            idle_time = current_time - data['last_seen']
            duration = round(data['last_seen'] - data['active_since'], 2)
            status = Text("ACTIVE", style="bold green") if idle_time <= 10 else Text("IDLE", style="bold red")
            
            if idle_time > 10:
                del active_hosts[ip]
            
            table.add_row(ip, received.hwsrc, status, str(duration))
        
        console.clear()
        console.print(table)
        time.sleep(5)

def monitor_ping(target_ip):
    """Continuously ping a host and track uptime, displaying in a table."""
    active_since = None
    last_seen = None
    
    while True:
        result = ping(target_ip, count=1, interval=0.5, timeout=2)
        current_time = time.time()
        
        if result.is_alive:
            if active_since is None:
                active_since = current_time
            last_seen = current_time
        else:
            if last_seen and current_time - last_seen > 10:
                active_since = None
                last_seen = None
        
        # Display table
        table = Table(title=f"Monitoring {target_ip}", show_lines=True)
        table.add_column("IP Address", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Active Duration (s)", justify="center")
        
        duration = round(last_seen - active_since, 2) if active_since else 0
        status = Text("ACTIVE", style="bold green") if active_since else Text("IDLE", style="bold red")
        
        table.add_row(target_ip, status, str(duration))
        
        console.clear()
        console.print(table)
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="OpenEye CLI - Continuous Network Monitoring Tool")
    parser.add_argument("--scan", help="Continuously scan a network (e.g., 192.168.1.0/24)")
    parser.add_argument("--ping", help="Continuously ping a host")
    args = parser.parse_args()
    
    if args.scan:
        scan_network(args.scan)
    elif args.ping:
        monitor_ping(args.ping)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
