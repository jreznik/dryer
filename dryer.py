import network
import dht
import machine
import socket
from time import sleep_ms

def main():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Fake-SSID', 'fake-password')

    d = dht.DHT11(machine.Pin(2))

    def http_get(url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        s.close()

    while True:
        d.measure()
        temp=d.temperature()
        http_get("https://dweet.io/dweet/for/rezza-dryer?temperature=" + str(temp))
        sleep_ms(1000)

if __name__ == "__main__":
    main()
