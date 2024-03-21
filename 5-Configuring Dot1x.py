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
    
    # Dot1x-G.txt content including additional configs
    dot1x_g_config = [
        "aaa new-model",
        "!",
        "radius server ISE1",
        " address ipv4 10.1.1.1 auth-port 1812 acct-port 1813",
        " key Cisco123",
        "!",
        "aaa group server radius ISE-RADIUS",
        " server name ISE1",
        "!",
        "aaa authentication dot1x default group ISE-RADIUS",
        "aaa authorization network default group ISE-RADIUS",
        "aaa accounting dot1x default start-stop group ISE-RADIUS",
        "aaa accounting system default start-stop group ISE-RADIUS",
        "!",
        "dot1x system-auth-control",
        "!",
        "radius-server vsa send accounting",
        "radius-server vsa send authentication"
    ]
    
    # Sending Dot1x-G.txt configuration
    output = myssh.send_config_set(dot1x_g_config)
    print(output)
    
    int_range = input('Specify the Interface(s) that needs to be configured with Dot1x [E0/0 or E 0/0-3 or E 0/0-2,E 1/0]: ')
    int_range_command = 'interface range ' + int_range
    
    # Dot1x-I.txt content
    dot1x_i_config = [
        "dot1x port-control auto",
        "dot1x reauthentication"
    ]
    
    # Sending Dot1x-I.txt configuration
    for LINE in dot1x_i_config:
        config_commands = [int_range_command, LINE]
        output = myssh.send_config_set(config_commands)
        print(output)

    switch_num -= 1
    print('Configured ' + x[1] + ' For Dot1x Authentication')

input('Press ENTER To Continue')
