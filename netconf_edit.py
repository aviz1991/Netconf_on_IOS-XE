from ncclient import manager
from router_info import csrv1000_1

#Reading the config from template ios-config1 xml file
config_template = open("ios-config1").read()
#Using the format method using the template and adding the missing items for config
netconf_config = config_template.format(interface_name="GigabitEthernet2",status="false")

with manager.connect(host=csrv1000_1["host"], port=csrv1000_1["port"], username=csrv1000_1["username"], password=csrv1000_1["password"], hostkey_verify=False) as m:
    device_reply = m.edit_config(netconf_config,target='running')
    print(device_reply)
