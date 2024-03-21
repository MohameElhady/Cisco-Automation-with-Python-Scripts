from netmiko import ConnectHandler

switch_num = input("How many switches would you like to configure: ")
switch_num = int(switch_num)

while switch_num > 0:
    hostip = input('Switch IP: ')
    USER = input('SSH Username: ')
    PASS = input('SSH Password: ')
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

    root = input('Would you like to configure ' + device + ' as a Root Switch for any VLAN: [y/n]: ')

    if root.lower() == 'y':
        vlans=input('Enter the VLAN that you would like the Switch to be Root For [1 or 1,2,10 or 1-10]: ')
        root_command='spanning-tree vlan ' + vlans + ' root primary'
        config_commands = [root_command]
        output = myssh.send_config_set(config_commands)
        print(output)

    root_sec = input('Would you like to configure ' + device + ' as a Secondary Root Switch for any VLAN: [y/n]: ')

    if root_sec.lower() == 'y':
        vlans=input('Enter the VLAN that you would like the Switch to be a Secondary Root For [1 or 1,2,10 or 1-10]: ')
        root_command='spanning-tree vlan ' + vlans + ' root secondary'
        config_commands = [root_command]
        output = myssh.send_config_set(config_commands)
        print(output)

    print('Switch \"' + device + '\" configured')
    print('-'*79)
    switch_num -=1

input("Press ENTER to finish")
