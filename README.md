# nmaptoexcel
An automated Python tool that runs Nmap scans and seamlessly exports discovered open ports and running services into a well-formatted Excel report for Penetration Testing.
# Nmap to Excel Scanner

This is an automated Python tool that streamlines network scanning using Nmap and seamlessly extracts the list of discovered open ports into a well-formatted Excel (`.xlsx`) report, making data reading and Penetration Testing reporting much easier.

## ✨ Key Features

- Automatically executes Nmap scans against target IPs (supports subnets).
- Performs service version detection (`-sV`).
- Automatically filters for ports with an `open` state.
- Exports data to an Excel file with standard columns: `IP Address`, `Protocol`, `Port`, `Service`, and `Remark`.
- Handles exceptions cleanly, alerting users if Nmap or required libraries are missing.

## 📋 Prerequisites

To run this tool, your system must have:
1. **Python 3**
2. **Nmap**: Ensure the `nmap` command can be executed directly from your terminal.
   - *On Kali/Debian/Ubuntu:* `sudo apt install nmap`
   - *On Windows:* Install using the official installer from the Nmap website and ensure it's added to your system's PATH environment variable.
3. Python libraries: `pandas`, `openpyxl`.

## ⚙️ Installation

Open your terminal and install the required Python libraries:

### For Windows / Standard Python Environments:
```bash
pip install pandas openpyxl
```

### For Kali Linux (or other OS using PEP 668 PIP restrictions):
If you encounter the `externally-managed-environment` error while using PIP, use one of the following methods:

**Method 1: Install via system APT (Recommended - Safe)**
```bash
sudo apt update
sudo apt install python3-pandas python3-openpyxl -y
```

**Method 2: Force PIP installation (Quick)**
```bash
pip install pandas openpyxl --break-system-packages
```

## 🚀 Usage

Basic tool syntax:
```bash
python nmap_to_excel.py -t <TARGET_IP> [-o <OUTPUT_EXCEL_FILE.xlsx>]
```

### Arguments:
- `-t` or `--target` *(Required)*: The target IP address or subnet you want to scan (e.g., `192.168.1.1` or `10.0.0.0/24`).
- `-o` or `--output` *(Optional)*: The output Excel filename. Defaults to `scan_results.xlsx` if not provided.

### Real-world Examples:

**1. Scan a single IP and save the results to `results.xlsx`:**
```bash
python nmap_to_excel.py -t 2.110.5.250 -o results.xlsx
```

**2. Scan an entire internal subnet using the default output filename:**
```bash
python nmap_to_excel.py -t 192.168.1.0/24
```

## 📊 Excel Output Format

Once the scan is complete, the generated Excel file will have the following 5-column structure:

| IP Address  | Protocol | Port | Service  | Remark                              |
|-------------|----------|------|----------|-------------------------------------|
| 2.110.5.250 | tcp      | 53   | domain   | Port 53/tcp was found to be open    |
| 2.110.5.250 | tcp      | 80   | http     | Port 80/tcp was found to be open    |
| 2.110.5.250 | tcp      | 443  | https    | Port 443/tcp was found to be open   |
