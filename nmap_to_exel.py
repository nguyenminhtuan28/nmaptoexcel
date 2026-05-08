import subprocess
import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys

def scan_and_export(targets, output_file)
    print(f[] Starting scan on target(s) {targets})
    print([] Please wait, the scan may take a while depending on the number of targets...)
    
    # Sử dụng nmap với đầu ra XML (-oX -)
    # -sV Dò tìm phiên bản dịch vụ đang chạy
    # -T4 Tăng tốc độ scan
    command = ['nmap', '-sV', '-T4', '-oX', '-', targets]
    
    try
        # Chạy lệnh nmap và lấy output
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        xml_output = result.stdout
    except subprocess.CalledProcessError as e
        print(f[-] Error executing nmap {e})
        print(f[-] Error details (stderr) {e.stderr})
        sys.exit(1)
    except FileNotFoundError
        print([-] ERROR 'nmap' command not found.)
        print([-] Please ensure Nmap is installed on your system and added to your PATH environment variable.)
        sys.exit(1)

    print([] Scan completed, processing results...)
    
    data = []
    
    try
        # Parse kết quả XML trả về từ nmap
        root = ET.fromstring(xml_output)
        
        for host in root.findall('host')
            ip_address = 
            for address in host.findall('address')
                if address.get('addrtype') == 'ipv4'
                    ip_address = address.get('addr')
            
            # Nếu không tìm thấy IP v4, có thể bỏ qua hoặc xử lý ipv6
            if not ip_address
                continue
                
            ports = host.find('ports')
            if ports is not None
                for port_element in ports.findall('port')
                    state_element = port_element.find('state')
                    
                    # Chỉ lấy những port có trạng thái là 'open'
                    if state_element is not None and state_element.get('state') == 'open'
                        protocol = port_element.get('protocol')
                        port_id = int(port_element.get('portid'))
                        
                        service_element = port_element.find('service')
                        service_name = service_element.get('name') if service_element is not None else unknown
                        
                        # Tạo cột Remark như yêu cầu
                        remark = fPort {port_id}{protocol} was found to be open
                        
                        data.append({
                            'IP Address' ip_address,
                            'Protocol' protocol,
                            'Port' port_id,
                            'Service' service_name,
                            'Remark' remark
                        })
    except ET.ParseError as e
        print(f[-] Error parsing XML data from nmap {e})
        sys.exit(1)

    if not data
        print([-] No open ports found on the specified targets.)
        return

    # Tạo DataFrame từ mảng dữ liệu
    df = pd.DataFrame(data)
    
    try
        # Xuất ra file Excel
        df.to_excel(output_file, index=False)
        print(f[+] SUCCESS! Exported {len(data)} open port results to file {output_file})
    except Exception as e
        print(f[-] Error writing to Excel file {e})
        print([-] Hint Ensure the 'openpyxl' library is installed so pandas can write Excel files.)
        print(    Install command pip install pandas openpyxl)

if __name__ == '__main__'
    parser = argparse.ArgumentParser(description=Tool to automatically scan with Nmap and export open ports to an Excel file.)
    parser.add_argument('-t', '--target', required=True, help=Target IP or IP range (e.g., 192.168.1.1 or 10.0.0.024))
    parser.add_argument('-o', '--output', default='scan_results.xlsx', help=Output Excel filename (default scan_results.xlsx))
    
    args = parser.parse_args()
    scan_and_export(args.target, args.output)
