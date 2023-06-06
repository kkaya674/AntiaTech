import random
from scipy.stats import rv_discrete
import pyaudio
import wave
import speech_recognition as sr
import _thread
import serial
import os,sys
import numpy as np
import RPi.GPIO as GPIO
import time
import socket
import re
import threading
import subprocess
from scapy.all import ARP, Ether, srp


def MACtoIP(target_ip="192.168.203.1/24"):

 
    
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    return clients
arg1 = sys.argv[1]

clients = MACtoIP(arg1)
print(clients)
