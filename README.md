# EyeNet 🌐👁️

**EyeNet** is a powerful and elegant command-line tool for real-time **network monitoring**. It can continuously scan your network to identify active devices or monitor the uptime of a specific host using ping. Built with Python, Scapy, icmplib, and Rich for interactive terminal visuals.

## ✨ Features

- 🔍 **ARP Scan Mode**: Continuously discovers active hosts in your local network.
- 📶 **Ping Monitor Mode**: Tracks the uptime and availability of a single device.
- 🧠 Smart detection of idle hosts (disappears after 10 seconds of inactivity).
- 🎨 Rich-based interactive terminal UI with status highlighting.
- ⏱️ Real-time tracking of how long a device has been online.

## 🛠️ Installation

Install the dependencies using pip:

```bash
pip install scapy icmplib rich
```

## 🚀 Usage

1. Scan Mode (Find Active Devices in Your Network)
```bash
sudo python eyenet.py --scan 192.168.1.0/24
```
This will continuously scan the given IP range and show a live table of active IPs, MAC addresses, and how long they’ve been online.

2. Ping Monitor Mode (Track Uptime of a Single Host)
```bash   
python eyenet.py --ping 8.8.8.8
```
This mode pings the target repeatedly and shows how long it has been reachable.

3. 📊 Output Example
```bash
+---------------+-------------------+---------+----------------------+
| IP Address    | MAC Address       | Status  | Active Duration (s)  |
+---------------+-------------------+---------+----------------------+
| 192.168.1.10  | 00:1A:2B:3C:4D:5E | ACTIVE  | 120.53               |
+---------------+-------------------+---------+----------------------+
```
Status will change to IDLE if the host is unreachable for over 10 seconds.

## 🧪 Tech Stack
	•	Python 3
	•	Scapy – for ARP scanning
	•	icmplib – for ICMP ping
	•	Rich – for beautiful terminal UI

## ⚠️ Permissions
	•	ARP scanning with Scapy requires root/admin access.
	•	Ping monitoring does not require elevated permissions.

## 📄 License

This project is licensed under the MIT License.
