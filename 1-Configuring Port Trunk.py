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
    print('Configuring ' + x[1])
    
    # Trunk interface range configuration
    int_range = input('Specify the Trunk Interface Range [e.g., E0/0 or E 0/0-3 or E 0/0-2,E 1/0]: ')
    trunk_config = [
        f'interface range {int_range}',
        'switchport trunk encapsulation dot1q',
        'switchport mode trunk',
        'switchport trunk allowed vlan all',
        'no shutdown'
    ]
    
    # Sending trunk interface range configuration
    output = myssh.send_config_set(trunk_config)
    print(output)
    
    switch_num -= 1
    print('Configured ' + x[1] + ' For Trunk Interface Range')

input('Press ENTER To Continue')
