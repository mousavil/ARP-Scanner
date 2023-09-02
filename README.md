
# Host Discovery

This script performs ARP scanning to discover live hosts on the local network. It sends ARP requests to a range of IP addresses and prints the IP and MAC address of any hosts that respond.

## Features

- Specify IP range to scan using start/end IPs or CIDR notation 
- Adjustable timeout for waiting for ARP responses
- Works on Linux by sending raw ARP packets (requires root/sudo)
- Gets current interface MAC address automatically
- Prints IP and MAC of any live hosts discovered

## Usage

```
usage: main.py [-h] [-s START_IP_ADDR] [-e END_IP_ADDR] [-r IP_RANGE [IP_RANGE ...]] [-w TIMEOUT] [-i INTERFACE]

optional arguments:
  -h, --help            show this help message and exit
  -s START_IP_ADDR, --start START_IP_ADDR
                        Start of IP range
  -e END_IP_ADDR, --end END_IP_ADDR
                        End of IP range
  -r IP_RANGE [IP_RANGE ...], --range IP_RANGE [IP_RANGE ...]
                        IP network range
  -w TIMEOUT, --wait TIMEOUT
                        Wait timeout seconds for ARP reply
  -i INTERFACE, --interface INTERFACE
                        Network interface name
```

Scan a range from 192.168.1.1 to 192.168.1.254:

```
sudo python main.py -s 192.168.1.1 -e 192.168.1.254
```

Scan a subnet in CIDR notation: 

```
sudo python main.py -r 192.168.1.0/24 
```

## How it Works

The script sends ARP requests using raw sockets at the data link layer. This allows sending custom Ethernet frames.

It first gets the MAC address of the specified interface using Linux sysfs.

The ARP request is ethernet frame containing the ARP payload. The source MAC is populated from the interface, and destination MAC is the broadcast address ff:ff:ff:ff:ff:ff.

It then waits for ARP replies and prints the IP and MAC of any responders.

## Warning

This script requires root/sudo on Linux to open raw sockets. Use care when running network scans.
