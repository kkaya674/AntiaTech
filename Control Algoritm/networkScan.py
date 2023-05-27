"""
If you want to use Wi-Fi instead of a wired Ethernet connection, you'll need to determine the name of your Wi-Fi network interface. The interface name for Wi-Fi can vary depending on the operating system and the Wi-Fi adapter you're using. Here are a few common interface names for Wi-Fi:

Linux: wlan0, wlp2s0, wlan1, etc.
macOS: en0, en1, en2, etc.
Windows: Wi-Fi, Wireless Network Connection, etc.
To find the interface name for Wi-Fi on your specific system, you can use the following steps:

Linux: You can use the iwconfig command or the ip command to list the available network interfaces. Look for an interface name starting with "wlan" or "wlp".

macOS: You can use the networksetup -listallhardwareports command in the terminal to list all network interfaces. Look for an interface labeled as Wi-Fi.

Windows: You can open the Command Prompt and use the netsh interface show interface command to list all network interfaces. Look for an interface labeled as Wi-Fi.

Once you have determined the correct Wi-Fi interface name for your system, replace 'eth0' in the previous code example with the appropriate Wi-Fi interface name. For example, if your Wi-Fi interface name is 'wlan0', the line should be:
"""



from scapy.all import ARP, Ether, srp
interface = "Wi-Fi"
thirdNumber =65

def scan_network(target_ip, interface):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=0.1, verbose=0, iface=interface)[0]
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices
#------------------------------------------------------------------------




def scanNetwork():
    deviceList = []
    for i in range(255):
        target_ip = "192.168.{}.{}".format(thirdNumber,i)
        devices = scan_network(target_ip, interface)
        if len(devices)!= 0:
            deviceList.append([devices[0]["ip"],devices[0]["mac"]])
    return deviceList
#------------------------------------------------------------------------




def main():
    i = 0
    while True:
        i+=1
        print("Trial : {}".format(i))
        deviceList = scanNetwork()
        print(deviceList)
        if len(deviceList)>1:
            break
main()