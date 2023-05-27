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