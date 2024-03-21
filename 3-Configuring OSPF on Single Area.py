from netmiko import ConnectHandler

router_num = input("How many routers would you like to configure: ")
router_num = int(router_num)

while router_num > 0:
    hostip = input('Router IP: ')
    USER = input('SSH Username: ')
    PASS = input('SSH Password: ')
    Router = {
        'device_type': 'cisco_ios',
        'ip': hostip,
        'username': USER,
        'password': PASS
    }

    myssh = ConnectHandler(**Router)
    hostname = myssh.send_command('show run | i host')
    x = hostname.split()
    device = x[1]

    ospfprocid = input('OSPF Process ID #: ')
    ospfrouterid = input('Router-ID: ')
    routerospf = 'router ospf ' + ospfprocid
    router_id = 'router-id ' + ospfrouterid
    network_num = input('How many networks would you like to enable in OSPF: ')
    network_num = int(network_num)
    config_commands = [routerospf,
                       router_id]
    output = myssh.send_config_set(config_commands)
    print(output)
    while network_num > 0:
        network_i = input('Please specify the network and mask to enable[10.1.0.0 0.0.255.255]: ')
        area_id = input('Enter the area to assign this network to: ')
        network_e = 'network ' + network_i + ' area ' + area_id
        config_commands = [routerospf,
                           network_e]
        output = myssh.send_config_set(config_commands)
        print(output)
        network_num -=1
    print('Router \"' + device + '\" configured')
    print('-'*79)
    router_num -=1

input("Press ENTER to finish")