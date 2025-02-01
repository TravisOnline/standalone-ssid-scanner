# standalone-ssid-scanner

## Background
Basic Python Wifi scanner. Will return access points' MAC address, SSID, channel and encryption.
Requires a wireless interface in monitoring mode as a CLI argument. This script will save all unique
access points to a .csv file where its run. I highly recommend using a Wide-Range Wireless Network 
Adapter with this script. Alfa produce a lot of great adapters with Kali/aircrack-ng compatible chipsets.

This script was written as a standalone component of another piece of work, with the intention to
provide a portable scanner that outputs to terminal and saves data to a local file.

## Usage
This script requires the following:
```commandline
- scapy and pandas python libraries
- root privileges in order to utilize scapy and airmon-ng
- a wireless interface in monitoring mode
```
`python collector.py wlanmon1` will run the script, scanning via wlanmon1 interface.

## Preparation
In order to set an interface to operate in monitoring mode, I suggest using airmon-ng. Please ensure that
other processes will not interrupt your interface or try to switch it off of monitoring mode. `airmon-ng check kill` will ensure this. 
Assuming you're scanning on an interface called wlan1, the follow commands will allow you to run this script:
```commandline
sudo airmon-ng check kill
airmon-ng start wlan1
airmon-ng
python collector.py wlanmon1
```
Terminal output is *very* messy when using a wide-range network adapter due to how the source file is written and read, and in conjunction with threading.
This is low priority as I'm just interested in the file output for another project sorry lol!
![alt text](https://i.kym-cdn.com/entries/icons/original/000/041/998/Screen_Shot_2022-09-23_at_10.40.58_AM.jpg)
