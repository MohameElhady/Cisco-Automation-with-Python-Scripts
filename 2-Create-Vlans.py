from netmiko import ConnectHandler

switch_num = int(input("How many switches would you like to configure: "))
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
    hostname = myssh.send_command('show run | inc host')
    x = hostname.split()
    device = x[1]
    print('Configuring VLANs on ' + x[1])
    
    # Configuring VLANs from 2 to 100
    vlan_config = []
    for vlan_id in range(2, 101):
        vlan_config.append(f'vlan {vlan_id}')
        vlan_config.append('name VLAN_' + str(vlan_id))
    
    # Sending VLAN configuration
    output = myssh.send_config_set(vlan_config)
    print(output)
    
    switch_num -= 1
    print('Configured VLANs on ' + x[1])

input('Press ENTER To Continue')
