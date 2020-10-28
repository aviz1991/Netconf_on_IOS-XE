from ncclient import manager

device = {
    'host':'192.168.108.10',
    'port': 830,
    'username': 'cisco',
    'password': 'cisco'
}

with manager.connect(host=device['host'],port=device['port'],username=device['username'],password=device['password'], hostkey_verify=False) as m:
    for capa in m.server_capabilities:
        print(capa)
