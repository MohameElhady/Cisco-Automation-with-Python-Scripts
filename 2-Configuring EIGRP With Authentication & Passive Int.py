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

    # Adding EIGRP authentication configuration
    auth_key = input('Enter MD5 authentication key: ')
    key_chain_name = input('Enter Key Chain name: ')
    key_chain = f'key chain {key_chain_name}\nkey 1\nkey-string {auth_key}'
    auth_command = f'ip authentication mode eigrp {eigrpas} md5'
    key_command = f'ip authentication key-chain eigrp {eigrpas} {key_chain_name}'

    # Configuring EIGRP authentication on interfaces
    network_num = input('How many networks would you like to enable in EIGRP: ')
    network_num = int(network_num)

    interface_auth_commands = []  # Initialize list to store interface authentication commands
    while network_num > 0:
        network_i = input('Please specify the network to enable: ')
        interface = input('Please specify the interface (e.g., GigabitEthernet0/0): ')
        if interface.lower() == 'skip':
            break

        # Skip loopback interface from authentication
        if 'loopback' in interface.lower():
            print(f'Skipping authentication for loopback interface {interface}')
            network_num -= 1
            continue

        # Adding EIGRP authentication configuration on non-loopback interfaces
        auth_interface_mode = input(f'Enable authentication on interface {interface}? (yes/no): ')
        if auth_interface_mode.lower() == 'yes':
            interface_auth_commands.extend([
                f'interface {interface}',
                auth_command,
                key_command
            ])

        # Configure passive interface if requested
        passive_interface = input(f'Configure {interface} as passive interface? (yes/no): ')
        if passive_interface.lower() == 'yes':
            passive_interface_command = f'passive-interface {interface}'
            interface_auth_commands.append(passive_interface_command)

        network_e = f'network {network_i}'
        config_commands = [routereigrp, network_e]
        output = myssh.send_config_set(config_commands, exit_config_mode=False)  # Avoid exiting config mode
        print(output)
        myssh.exit_config_mode()  # Ensure exiting config mode before proceeding
        network_num -= 1

    # Apply authentication configuration if at least one interface has been configured for authentication
    if interface_auth_commands:
        config_commands = [routereigrp] + interface_auth_commands
        output = myssh.send_config_set(config_commands, exit_config_mode=False)
        print(output)

    # Configure key chain in global configuration mode
    key_chain_config = [f'key chain {key_chain_name}', 'key 1', f'key-string {auth_key}']
    output = myssh.send_config_set(key_chain_config)
    print(output)

    print('Router \"' + device + '\" configured')
    print('-' * 79)
    router_num -= 1

input("Press ENTER to finish")
