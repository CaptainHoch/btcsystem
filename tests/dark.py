import requests
from stem import Signal
from stem.control import Controller
proxies = {
    'http': 'socks5://localhost:9050',
    'https': 'socks5://localhost:9050'
}
url = 'http://httpbin.org/ip'
print(requests.get(url, proxies=proxies).text)

def renewIP():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='zaq12wsx')
        controller.signal(Signal.NEWNYM)

renewIP()
