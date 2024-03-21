from netmiko import ConnectHandler

def configure_router(router_ip, username, password):
    Router = {
        'device_type': 'cisco_ios',
        'ip': router_ip,
        'username': username,
        'password': password
    }
    myssh = ConnectHandler(**Router)

    ospfprocid = input('OSPF Process ID #: ')
    ospfrouterid = input('Router-ID: ')
    area_id = input('Area ID: ')

    routerospf = 'router ospf ' + ospfprocid
    router_id = 'router-id ' + ospfrouterid

    config_commands = [routerospf,
                       router_id]
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
                network_e = 'network ' + x[1] + ' 0.0.0.0' + ' area ' + area_id
                config_commands.append(network_e)

                is_passive = input(f'Is interface {x[0]} passive? (yes/no): ').lower()
                if is_passive == 'yes':
                    passive_interface = 'passive-interface ' + x[0]
                    config_commands.append(passive_interface)

                output=myssh.send_config_set(config_commands)
                print(output)
    print('Router "' + device + '" configured')
    print('-' * 79)

router_num = input("How many routers would you like to configure: ")
router_num = int(router_num)

for _ in range(router_num):
    hostip = input('Router IP: ')
    USER = input('SSH Username: ')
    PASS = input('SSH Password: ')
    configure_router(hostip, USER, PASS)

input("Press ENTER to finish")
