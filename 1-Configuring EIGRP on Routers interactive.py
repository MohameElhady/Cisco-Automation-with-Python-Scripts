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

    eigrpas = input('EIGRP AS #: ')
    routereigrp = 'router eigrp ' + eigrpas
    network_num = input('How many networks would you like to enable in EIGRP: ')
    network_num = int(network_num)
    while network_num > 0:
        network_i = input('Please specify the network to enable: ')
        network_e = 'network ' + network_i
        config_commands = [routereigrp,
                           network_e]
        output = myssh.send_config_set(config_commands)
        print(output)
        network_num -=1
    print('Router \"' + device + '\" configured')
    print('-'*79)
    router_num -=1

input("Press ENTER to finish")