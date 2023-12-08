# ePDG + N3IWF discoverer
Resolves the IP addresses of ePDGs or N3IWFs from most mobile operators in the world and checks if each responds to ICMP and whether it accepts IKEv2 connection.

---
---
This is a fork from https://github.com/mrlnc/epdg_discoverer by @mrlnc 

Note: the original code by @Spinlogic is available here: https://github.com/Spinlogic/epdg_discoverer

My repo introduces checks for N3IWF (5G)

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

# Dependencies

Install dependencies:
```
python3 -m venv .venv
source .venv/bin/actiate
pip3 install < requirements.txt
```

Fetch the network list:
```
./get_operator_list.py network-list.txt
```

## Usage
```
sudo .venv/bin/python3 vowifi_scanner.py <network-list> <output-file>
```

Note that the ePDG/N3IWF address of some operators is resolved, but it does not respond to neither ICMP nor IKEv2_SA_INIT messages. This could mean that the service is off, geoblocked, or does not like the received request and drops it (if it is an IKEv2 one, specially). 
