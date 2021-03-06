from ncclient import manager
from pprint import pprint
import xmltodict
import xml.dom.minidom
# import logging
# logging.basicConfig(level=logging.DEBUG)

router = {"host": "192.168.108.10", "port": "830",
          "username": "cisco", "password": "cisco"}
print(router["host"])
print(router["port"])
print(router["username"])
print(router["password"])

netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>Loopback0</name>
    </interface>
  </interfaces>
  <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet1</name>
    </interface>
  </interfaces-state>
</filter>
 """

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
    for capability in m.server_capabilities:
        print('*' * 50)
        print(capability)
    # get the running config on the filtered out interface
    print('Connected')
    interface_netconf = m.get(netconf_filter)
    print('getting running config')
# below, xml is a property of interface_conf

# XMLDOM for formatting output to xml
xmlDom = xml.dom.minidom.parseString(str(interface_netconf))
print(xmlDom.toprettyxml(indent="  "))
print('*' * 25 + 'Break' + '*' * 50)
# XMLTODICT for formatting xml output to a python dictionary
interface_python = xmltodict.parse(interface_netconf.xml)[
    "rpc-reply"]["data"]
pprint(interface_python)
name = interface_python['interfaces']['interface']['name']['#text']
print(name)
ip = interface_python['interfaces']['interface']['ipv4']['address']['ip']
print(ip)

config = interface_python['interfaces']['interface']
op_state = interface_python['interfaces-state']['interface']

print("start")
print(f"Name:{config['name']['#text']}")
print(f"Description: {config['description']}")
print(f"Packets in {op_state['statistics']['in-unicast-pkts']}")
print(f"packets in in-octets {op_state['statistics']['in-octets']}")
