# ePDG + N3IWF discoverer
Resolves the IP addresses of ePDGs or N3IWFs from most mobile operators in the world and checks if each responds to ICMP and whether it accepts IKEv2 connection.

---
---
This is a fork from https://github.com/mrlnc/epdg_discoverer by @mrlnc 

Note: the original code by @Spinlogic is available here: https://github.com/Spinlogic/epdg_discoverer

My repo introduces several improvements and checks for N3IWF as well (5G)

---
---

## ePDG address resolution
Mobile networks use a pre-defined pattern for their ePDG:

> epdg.epc.mcc<_mcc_>.mnc<_mnc_>.pub.3gppnetwork.org

For example, Spain has mcc = 214 and Movistar (Telefónica) has mnc = 07 in Spain. Therefore the URI for Movistar ePDG's is:

> epdg.epc.mcc214.mnc007.pub.3gppnetwork.org

The script resolves both IPv4 and IPv6, but supports only IPv4 hosts for IKEv2 discovery.

## N3IWF address resolution
5G Mobile networks use a pre-defined pattern for their N3IWF:

> n3iwf.5gc.mcc<_mcc_>.mnc<_mnc_>.pub.3gppnetwork.org

# Installation (venv)

Install python >3.8 if not in the system. Then also install

```
sudo apt install python3.8-venv
sudo apt install python3-wheel 
```

Install dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Fetch the network list:
```
./get_operator_list.py network-list.txt
```

## Usage
```
sudo ./vowifi_scanner.py <network-list> <output-file> [5g]
```

Appending 5g at the end of the command, will switch from ePDG to N3IWF scan. This will take a while as the script will check all operators in the network-list CSV file (at present 2970 entries).

Note that the ePDG/N3IWF address of some operators is resolved, but it does not respond to neither ICMP nor IKEv2_SA_INIT messages. This could mean that the service is off, geoblocked, or does not like the received request (i.e., unsupported ENCR/PRF/INTEG/D-H proposals or keys in IKEv2_SA_INIT, or firewall with rate limits) and drops it. Now the IKEv2_SA_INIT is improved to reduce missing responses, reflecting the same message from a Xiaomi phone. 
