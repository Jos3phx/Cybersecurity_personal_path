# 🛡️ arp_poison.py — ARP Cache Poisoning & MITM Lab Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-2.5.0%2B-green?style=flat-square)
![Focus](https://img.shields.io/badge/Network_Security-Layer_2_%2F_ARP-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

Educational **ARP Spoofing / ARP Cache Poisoning** tool built in Python using **Scapy**. Originally inspired by Chapter 4 of *Black Hat Python (2nd Edition)*, this implementation has been refactored and hardened for stability, clean process management, and compatibility with modern Linux and Python (3.9–3.14+) environments.

> [!WARNING]
> **Authorized Lab Use Only:** Read the [Legal & Ethical Disclaimer](#️-legal--ethical-disclaimer) carefully before executing this tool. Never run ARP spoofing on networks without explicit, written permission.

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


[!TIP]
Virtual Machine Users (VirtualBox / VMware): Configure your network adapter in Bridged Mode and set Promiscuous Mode to Allow All. Default NAT or strict hypervisor MAC filtering will block spoofed frames from leaving the virtual interface.
