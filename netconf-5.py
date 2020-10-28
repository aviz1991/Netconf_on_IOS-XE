from ncclient import manager
from pprint import pprint
import xmltodict
import xml.dom.minidom
from router_info import all_devices

# import logging
# logging.basicConfig(level=logging.DEBUG)

#Here the yang model which is the xml filter are created in a new file and read here instead of adding in script
netconf_filter = open("netconf_filter.xml").read()

for router in all_devices:
    with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
         #for capability in m.server_capabilities:
          #   print('*' * 50)
           #  print(capability)
    # get the running config on the filtered out interface
         print(f'Connected to device {router["name"]}')
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

    print("starting to printing for ")
    print(f"Name:{config['name']['#text']}")
    print(f"Description: {config['description']}")
    print(f"Packets in {op_state['statistics']['in-unicast-pkts']}")
    print(f"packets in in-octets {op_state['statistics']['in-octets']}")