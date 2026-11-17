# 🛡️ arp_poison.py — ARP Cache Poisoning & MITM Lab Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-2.5.0%2B-green?style=flat-square)
![Focus](https://img.shields.io/badge/Network_Security-Layer_2_%2F_ARP-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

Educational **ARP Spoofing / ARP Cache Poisoning** tool built in Python using **Scapy**. Originally inspired by Chapter 4 of *Black Hat Python (2nd Edition)*, this implementation has been refactored and enhanced with the assistance of the AI ​​Claude Code to ensure greater stability, clean process management, and compatibility with modern Linux and Python (3.9–3.14+) environments.

> [!WARNING]
> ⚠️ **Authorized Lab Use Only:** Read the [Legal & Ethical Disclaimer](#-legal--ethical-disclaimer) and the [LICENSE](LICENSE) terms carefully before executing this tool. Never run ARP spoofing on networks without explicit, written permission.

---

## 🌐 How It Works (Layer 2 Mechanics)

The Address Resolution Protocol (ARP) lacks built-in authentication, allowing any host on a local broadcast domain to send unsolicited ARP replies (`is-at`) and overwrite the ARP cache of neighboring devices. `arp_poison.py` automates this process in five stages:

1. 🔎 **MAC Address Resolution:** Sends broadcast Layer 2 ARP `who-has` frames (`srp`) to resolve the hardware addresses of both the **target host** and the **default gateway**.
2. 💉 **Bidirectional Cache Poisoning:** Continuously transmits forged Layer 2 ARP replies (`op=2`) via `sendp()`:
   - Tells the **victim** that the gateway's IP resides at the attacker's MAC address.
   - Tells the **gateway** that the victim's IP resides at the attacker's MAC address.
3. 🔀 **Traffic Interception (MITM):** With IPv4 forwarding enabled on the attacker host, traffic between the target and the gateway flows transparently through the attacker's network interface.
4. 📡 **Packet Capture (Optional):** Spawns a parallel sniffer worker filtering traffic for `host <victim>` and exports captured frames to a `.pcap` file for offline inspection in Wireshark or `tcpdump`.
5. 🧹 **Graceful ARP Restoration:** Upon receiving `SIGINT` (`Ctrl+C`), halts child workers cleanly and sends directed Layer 2 ARP replies to restore the legitimate MAC-to-IP mappings on both ends.

---

## ⚙️ Prerequisites & Lab Environment

- 🐧 **Operating System:** Linux (tested on Ubuntu / Kali Linux)
- 🐍 **Python:** 3.9+ (tested up to Python 3.14)
- 🔑 **Privileges:** Root (`sudo`) required for raw socket access and Layer 2 frame injection
- 🔄 **IPv4 Forwarding:** Must be enabled on the attacker machine so intercepted traffic is routed rather than dropped:
  ```bash
  sudo sysctl -w net.ipv4.ip_forward=1
  ```

> [!TIP]
> 💡 **Virtual Machine Users (VirtualBox / VMware):** Configure your network adapter in **Bridged Mode** and set **Promiscuous Mode** to **Allow All**. Default NAT or strict hypervisor MAC filtering will block spoofed frames from leaving the virtual interface.

---

## 📦 Installation

```bash
git clone [https://github.com/Jos3phx/Cybersecurity_personal_path.git](https://github.com/Jos3phx/Cybersecurity_personal_path.git)
cd Cybersecurity_personal_path/01_Python_Security_Tools/arp_poison
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
sudo python3 arp_poison.py <VICTIM_IP> <GATEWAY_IP> <INTERFACE> [options]
```

### 💻 Basic Example

```bash
sudo python3 arp_poison.py 192.168.1.5 192.168.1.1 eth0
```

### 🎛️ CLI Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--interval` | Delay between forged ARP bursts (in seconds) | `2.0` |
| `--sniff-count` | Maximum number of packets to capture | `100` |
| `--output` | Output `.pcap` filename | `arper.pcap` |
| `--no-sniff` | Disable packet capture and run ARP poisoning only | `False` |
| `--yes` / `-y` | Skip interactive authorization confirmation prompt | `False` |
| `--verbose` / `-v` | Enable detailed `DEBUG` logging output | `False` |
| `--help` / `-h` | Display help message and exit | — |

### 🔍 Custom Capture Example

```bash
sudo python3 arp_poison.py 192.168.1.5 192.168.1.1 eth0 \
  --interval 1 --sniff-count 200 --output mitm_lab.pcap -v
```

Press `Ctrl+C` at any time to stop the attack and automatically restore the ARP tables.

---

## 🧪 Lab Verification

On the target machine, inspect the ARP cache before, during, and after executing the script:

```bash
# Linux
ip neigh show

# Windows / Cross-platform
arp -a
```

- **During execution:** The gateway's IP entry on the target maps to the **attacker's MAC address**.
- **After `Ctrl+C`:** The entry automatically reverts to the **legitimate router MAC address**.

---

## 🔧 Technical Notes & Fixes Over the Original Book Implementation

Several stability issues present in legacy Scapy/Python implementations were resolved in this version:

- **Explicit Layer 2 Framing (`sendp` vs. `send`):** Using Layer 3 `send()` for ARP triggers Scapy Ethernet destination warnings and relies on automatic L2 resolution. All poison and restore packets explicitly wrap `Ether(dst=<target_mac>) / ARP(...)` and transmit via `sendp()`.
- **Python 3.14+ `multiprocessing` Compatibility:** Starting in Python 3.14, Linux changed the default multiprocessing start method from `fork` to `forkserver`, which attempts to pickle bound class methods and raises `TypeError: cannot pickle 'weakref.ReferenceType' object`. Calling `set_start_method("fork")` explicitly ensures reliable process spawning.
- **Clean `SIGINT` (`Ctrl+C`) Coordination:** In the original code, `KeyboardInterrupt` propagated unpredictably to child processes during `time.sleep()`, generating unhandled tracebacks. Here, child workers ignore `SIGINT` (`signal.SIG_IGN`) while the parent traps `SIGINT` to set a shared `multiprocessing.Event()`. Child loops exit immediately via `stop_event.wait()`, and `restore()` runs once inside the parent's `finally` block.
- **Non-Blocking Packet Sniffing:** Instead of a single blocking `sniff(count=100)` call that hangs indefinitely on quiet networks, packets are captured in short batches (`timeout=2`), allowing the sniffer process to check `stop_event` and terminate cleanly even if zero packets match the BPF filter.

---

## ⚖️ Legal & Ethical Disclaimer

This tool performs active network traffic interception via ARP Spoofing.

- **Authorized Use Only:** Execute this script strictly within isolated home labs or against networks and systems where you hold **explicit, written authorization**.
- **Legal Responsibility:** Unauthorized interception of network communications is illegal and punishable under applicable cybercrime statutes (including Brazilian Law 12.737/2012 and the Brazilian Civil Rights Framework for the Internet).
- The author assumes no liability for misuse, network disruption, or legal consequences resulting from the unauthorized operation of this software.

---

## 📄 License

Distributed under the **MIT License** — see [LICENSE](LICENSE) for full terms and conditions.
