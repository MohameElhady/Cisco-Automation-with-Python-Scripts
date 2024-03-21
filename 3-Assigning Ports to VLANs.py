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

    vlan_num = input('How many VLANs would you like to Configure: ')
    vlan_num = int(vlan_num)
    while vlan_num > 0:
        vlan = input('VLAN ID: ')
        int_range = input('Specify the Interface(s) that need to configured in vlan ' + vlan + ' [E0/0 or E 0/0-3 or E 0/0-2,E 1/0]: ' )
        int_range_command = 'interface range ' + int_range
        access_command = 'switchport access vlan ' + vlan
        config_commands = [int_range_command, 'switchport mode access',
                           'spanning-tree portfast',
                           access_command]
        output = myssh.send_config_set(config_commands)
        print(output)
        vlan_num -=1
    print('Switch \"' + device + '\" configured')
    print('-'*79)
    switch_num -=1

input("Press ENTER to finish")