import subprocess
import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys


def scan_and_export(targets, output_file):
    print(f"[+] Starting scan on target(s): {targets}")
    print("[*] Please wait, the scan may take a while depending on the number of targets...")

    command = ["nmap", "-sV", "-T4", "-oX", "-", targets]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
        xml_output = result.stdout

    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing nmap: {e}")
        print(f"[-] Error details (stderr): {e.stderr}")
        sys.exit(1)

    except FileNotFoundError:
        print("[-] ERROR: 'nmap' command not found.")
        print("[-] Please install Nmap first.")
        sys.exit(1)

    print("[+] Scan completed, processing results...")

    data = []

    try:
        root = ET.fromstring(xml_output)

        for host in root.findall("host"):
            ip_address = ""

            for address in host.findall("address"):
                if address.get("addrtype") == "ipv4":
                    ip_address = address.get("addr")

            if not ip_address:
                continue

            ports = host.find("ports")

            if ports is not None:
                for port_element in ports.findall("port"):
                    state_element = port_element.find("state")

                    if state_element is not None and state_element.get("state") == "open":
                        protocol = port_element.get("protocol")
                        port_id = int(port_element.get("portid"))

                        service_element = port_element.find("service")
                        service_name = (
                            service_element.get("name")
                            if service_element is not None
                            else "unknown"
                        )

                        remark = f"Port {port_id}/{protocol} was found to be open"

                        data.append({
                            "IP Address": ip_address,
                            "Protocol": protocol,
                            "Port": port_id,
                            "Service": service_name,
                            "Remark": remark
                        })

    except ET.ParseError as e:
        print(f"[-] Error parsing XML data from nmap: {e}")
        sys.exit(1)

    if not data:
        print("[-] No open ports found on the specified targets.")
        return

    df = pd.DataFrame(data)

    try:
        df.to_excel(output_file, index=False)
        print(f"[+] SUCCESS! Exported {len(data)} open port results to file: {output_file}")

    except Exception as e:
        print(f"[-] Error writing to Excel file: {e}")
        print("[-] Hint: install openpyxl with:")
        print("    pip install pandas openpyxl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to scan with Nmap and export open ports to an Excel file."
    )

    parser.add_argument(
        "-t",
        "--target",
        required=True,
        help="Target IP, IP range, or comma-separated IPs"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="scan_results.xlsx",
        help="Output Excel filename"
    )

    args = parser.parse_args()
    scan_and_export(args.target, args.output)
