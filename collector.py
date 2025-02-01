import csv
from importlib.resources.readers import remove_duplicates

import pandas
from threading import Thread
import time
import os
import sys
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt
from scapy.sendrecv import sniff

network_holder = pandas.DataFrame(columns=["BSSID", "SSID", "Channel", "Crypto"])
network_holder.set_index("BSSID", inplace=True)

_localfile = "null"

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # extract SSID name
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats for Channel and Crypto
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        network_holder.loc[bssid] = (ssid, channel, crypto)
        # global _tempfile
        global _localfile
        network_holder.to_csv(_localfile, mode='a', index=True, header=False)
        remove_duplicates()

def remove_duplicates():
    global _localfile
    # global _tempfile

    lf = pandas.read_csv(_localfile).drop_duplicates('SSID',keep='first')
    lf.index_col=False
    lf.to_csv(_localfile, index=False, header=True)

# Cycle through wifi channels 1-14 every half second
def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch % 13 + 1
        time.sleep(0.5)

def print_all():
    global _localfile
    while True:
        os.system("clear")
        try:
            print(pandas.read_csv(_localfile))
        except:
            print("Loading CSV")
        time.sleep(0.5)

def create_wifi_csv():
    try:
        # Check for SSIDs.csv
        f = open("SSIDs.csv")
    except FileNotFoundError:
        # Create SSIDs.json if not found
        with open("SSIDs.csv", "w") as f:
            f.write("BSSID,SSID,Channel,Crypto\n")
            f.close()
            pass
    global _localfile
    if _localfile == "null":
        _localfile = "SSIDs.csv"

if __name__ == "__main__":
    # Interface name set by "aircrack-ng start wlan0"
    try:
        interface = str(sys.argv[1])
    except:
        print("Invalid or no interface provided.")
        print("In order to run this tool, use:")
        print("collector.py [interface]")
        exit()
    create_wifi_csv()
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()

    # start channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    # Start sniffing
    sniff(prn=callback, iface=interface)
