# 🔍 Custom TCP & UDP Port Scanner

Custom Python-based multi-protocol network scanner designed to perform fast TCP connection attempts and UDP socket probes to identify open services across target IP addresses.

---

## 🎯 Plan Alignment
* **Roadmap Section:** 1st Quarter - Month 01 (Programming & Automation)
* **Core Focus:** Network Sockets, Transport Layer Protocols (TCP/UDP), Python I/O.

---

## 📋 Features
- **TCP Connect Scanning:** Checks state of target TCP ports via 3-way handshake simulation.
- **UDP Scanning:** Sends protocol-specific payload probes to detect open/filtered UDP ports.
- **Custom Timeout & Threads:** Optimized socket timeouts to reduce scan duration.

---

## 🛠️ Technical Implementation & Purpose
This tool was built to understand the low-level behavior of network sockets without relying on external third-party scanner binaries. It demonstrates:
- Manipulating standard Python `socket` module.
- Handling connection exceptions (`socket.timeout`, `socket.error`).
- Parsing command-line arguments for custom target ranges.
