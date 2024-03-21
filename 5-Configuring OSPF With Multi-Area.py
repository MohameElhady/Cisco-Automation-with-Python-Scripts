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

    ospfprocid = input('OSPF Process ID #: ')
    ospfrouterid = input('Router-ID: ')
    routerospf = 'router ospf ' + ospfprocid
    router_id = 'router-id ' + ospfrouterid

    config_commands = [routerospf,
                       router_id ]
    output = myssh.send_config_set(config_commands)
    print(output)

    hostname = myssh.send_command('show run | i host')
    x = hostname.split()
    device = x[1]
    SIIB = myssh.send_command('show ip int brief')

    log_file = open('TEMP.txt', "w")
    log_file.write(SIIB)
    log_file.write("\n")
    log_file.close()
    file_a = open('TEMP.txt', "r")
    lines = file_a.readlines()
    file_a.close()

    del lines[0]

    int_file = open('TEMP.txt', "w+")

    for line in lines:
        int_file.write(line)
    int_file.close()

    with open('TEMP.txt') as FILE:
        for LINE in FILE:
            x=LINE.split()
            if (x[1] == 'IP-Address') or (x[1] == 'unassigned'):
                pass
            else:
                area_id = input('Area ID for ' + x[1] + ": ")
                network_e = 'network ' + x[1] + ' 0.0.0.0' + ' area ' + area_id
                config_commands = [routerospf,
                                   network_e]
                output=myssh.send_config_set(config_commands)
                print(output)
    router_num -=1
    print('Router "' + device + '" configured')
    print('-' * 79)

input("Press ENTER to finish")