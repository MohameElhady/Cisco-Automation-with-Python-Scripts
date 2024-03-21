from netmiko import ConnectHandler

switch_num = input("How many switches would you like to configure: ")
switch_num = int(switch_num)

USER = input('SSH Username: ')
PASS = input('SSH Password: ')

while switch_num > 0:
    hostip = input('Switch IP: ')
    Switch = {
        'device_type': 'cisco_ios',
        'ip': hostip,
        'username': USER,
        'password': PASS
    }

    myssh = ConnectHandler(**Switch)
    hostname = myssh.send_command('show run | i host')
    x = hostname.split()
    device = x[1]

    sticky = input('Would you like to configure Sticky Mode: [y/n]')

    if sticky.lower() == 'y':
        int_range = input('Specify the Interface(s) that needs to configured with Port Security [E0/0 or E 0/0-3 or E 0/0-2,E 1/0]: ')
        int_range_command = 'interface range ' + int_range
        config_commands = [int_range_command, 'switchport mode access',
                           'switchport port-security', 'switchport port-security mac sticky']
        output = myssh.send_config_set(config_commands)
        print(output)
    else:
        int_num = input('Specify the Number of Interface that needs to configured with Static Port Security: ')
        int_num = int(int_num)
        while int_num >0:
            int_id = input('Specify the Interface that needs to configured with Static Port Security [E0/0]: ')
            int_id_command = 'interface ' + int_id
            mac_addr = input('MAC Address for Interface ' + int_id + ' [xxxx.xxxx.xxxx]: ')
            port_security_command = 'switchport port-security mac ' + mac_addr
            config_commands = [int_id_command, 'switchport mode access',
                               'switchport port-security', port_security_command]
            output = myssh.send_config_set(config_commands)
            print(output)
            int_num -= 1

    print('Switch \"' + device + '\" configured')
    print('-'*79)
    switch_num -=1

input("Press ENTER to finish")