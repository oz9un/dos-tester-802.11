
# DoS-Tester 802.11

It's a Python tool that tests some DoS attacks on 802.11 networks with flooding desired packets. Developed with Scapy. 

It provides an easy command-line-interace that users can easily inject packets and test their networks.
## Current Features (v1) 😈

DoS Tester successfully performs the following attacks:

- **Authentication Request Flood:**
    
    It is an attack that targets the access point. It fills the buffer of the target access point with flooding new connections, the AP is depleted of resources and becomes unavailable to service for legit clients. 
    
- **Association Request Flood**

    In this attack, where both access points and clients can be received as a target, the access point sends 'Deauthentication' packets to the source address of 'Association Request' packets. 

    Thus, clients on the line can be disconnected by this method. Very cool way to perform **deauth attack! 😎**.

    While performing these operations, the resources of the access point, which has to constantly check the 'Authentication' status of the source addresses, are restricted. 

- **Probe Request Flood**

    This attack can be used for two purposes:

    1. The attacker keeps access points busy with many 'Probe Request' packets that sent to the target access point and consumes his resources. (Access points will try to respond with 'Probe Response' to all request packets.)

    2. With some kind of 'brute-forcing attack', attacker tries to find SSID's of hidden networks with flooding 'Probe Request' packets.
  
## Arguments & Example Usages 💬

DoS-Tester has six arguments:

1. **-src (--source_address)**: Source address of the packet (MAC).

2. **-dst (--destination_address)**: Destination address of the packet (MAC).

3. **-p (--packet_type)**: Type of the 802.11 packet. Current choices "authReq", "assocReq", "probeReq".

4. **-c (--count)**: Number of packets to sent.

5. **-i (--interface)**: Interface name (must be in monitor mode).

6. **-ssid (--ssid)**: (_Required for AssocReq, Optional for ProbeReq_) SSID of target AP. 




**probeReq:**
```bash
└─$ sudo python3 dos_tester.py -src 0b:0d:01:02:00:00 -dst FF:FF:FF:FF:FF:F1 -i wlan0mon -p probeReq -c 50
```
**authReq:**
```bash
└─$ sudo python3 dos_tester.py -src 0b:0d:01:02:00:00 -dst 22:22:22:11:11:11 -i wlan0mon -p authReq -c 190
```
**assocReq:**
```bash
└─$ sudo python3 dos_tester.py -src 0b:0d:01:02:00:00 -dst 44:22:2b:aa:11:11 -i wlan0mon -p assocReq -c 50 -ssid "oz9un!"
```
**beacon: send a beacon packet every 100 milliseconds, not works with count right now.**
```bash
└─$ sudo python3 dos_tester.py -dst "FF:FF:FF:FF:FF:FF" -src "C2:45:21:FF:FF:FF" -ssid "BeaconBomb" -i wlan0mon -p beacon
```

  
## Help Menu 👼

![Help Menu](https://i.ibb.co/V2ghDwq/Screenshot-408.png)


## Upcoming Features 🔜

- [x] **Beacon Flood**

- [ ] **Disassociation Flood**

- [ ] **Deauthentication Flood**

- [ ] **EAPOL Start-Logoff Flood 🐐**

## Example Screenshots :camera_flash:

- **Beacon Flood:** 

![image](https://user-images.githubusercontent.com/57866851/120047708-e4320500-c01d-11eb-920e-55a6094d5569.png)


## Disclaimer ⛔

All information and software available on this page are for educational and test purposes only. Use these at your own discretion, the repository owners cannot be held responsible for any damages caused.

Usage of all tools on this repository for attacking targets without prior mutual consent is illegal. It is the end user’s responsibility to obey all applicable local, state and federal laws. We assume no liability and are not responsible for any misuse or damage caused by this repository.
