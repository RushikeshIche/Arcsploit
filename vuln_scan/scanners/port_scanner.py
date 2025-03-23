import nmap
import time
from ..utils.logger import log_vulnerability

def scan_ports(target):
    try:
        nm = nmap.PortScanner()

       
        print("\nScan Types:")
        print("1.Quick Scan (Fast, Limited Ports)")
        print("2.Aggressive Scan (More Details)")
        print("3.Full Scan (All 65535 Ports)")

        choice = input("\n Choose scan type (1/2/3): ").strip()
	
        if choice == "1":
            scan_args = "-sV -F" 
            scanType="Quick Scan"
        elif choice == "2":
            scan_args = "-sV -O"  
            scanType="Aggressive Scan"
        elif choice == "3":
            scan_args = "-sV -p-" 
            scanType="Full Scan"
        else:
            print("Invalid choice! Defaulting to Quick Scan.")
            scan_args = "-sV -F"
            scanType="Quick Scan"

        print(f"\nScanning {target} with option: {scanType} ...")
        start_time = time.time()

       
        nm.scan(target, arguments=scan_args)

        scan_duration = round(time.time() - start_time, 2)
        print(f"\nScan Completed in {scan_duration} seconds.\n")

        
        results = []
        for host in nm.all_hosts():
            print(f"\nHost: {host} ({nm[host].hostname() or 'Unknown'})")
            print("Open Ports:")

            for proto in nm[host].all_protocols():
                print(f"   Protocol: {proto.upper()}")

                ports = nm[host][proto].keys()
                for port in sorted(ports):
                    data = nm[host][proto][port]
                    results.append({
                        "port": port,
                        "protocol": proto,
                        "state": data['state'],
                        "service": data.get('name', 'Unknown'),
                        "product": data.get('product', 'N/A'),
                        "version": data.get('version', 'N/A')
                    })
                    
                    log_vulnerability(f"     {port}/{proto.upper()} - {data['state']} ({data.get('name', 'Unknown')} {data.get('version', '')})")

     
        if not results:
        	print("No open ports Found.\n")
        	
        return results

    except Exception as e:
        print(f" Error: {str(e)}")
        return []
