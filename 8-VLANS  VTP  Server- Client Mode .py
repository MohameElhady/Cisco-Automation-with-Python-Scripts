from netmiko import ConnectHandler

# Define the list of switch IP addresses
switch_ips = ['192.168.8.101', '192.168.8.102', '192.168.8.103']

# Prompt for SSH username and password
USER = input('SSH Username: ')
PASS = input('SSH Password: ')

# Iterate over each switch IP address
for ip in switch_ips:
    print('Configuring ' + ip + '-' * 30)
    
    # Define the switch dictionary for Netmiko
    Switch = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': USER,
        'password': PASS
    }
    
    # Establish SSH connection to the switch
    myssh = ConnectHandler(**Switch)
    
    # Get the hostname of the switch
    hostname = myssh.send_command('show run | i host')
    x = hostname.split()
    devicename = x[1]

    # Prompt for VTP mode and domain
    vtp_mode = input('Specify VTP Mode [Server | Client]: ')
    vtp_domain = input('VTP Domain: ')
    vtp_domain_command = 'vtp domain ' + vtp_domain
    
    # Configure switch based on VTP mode
    if vtp_mode.lower() == 'server':
        vlans = input('Enter the VLANs you would like to create [1 or 1,2,10 or 1-10]: ')
        print('Configuring ' + devicename + ' as a VTP Server with VLANs ' + vlans)
        vlan_command = 'vlan ' + vlans
        config_commands = ['vtp mode server', vtp_domain_command, vlan_command]
        output = myssh.send_config_set(config_commands)
        print(output)
    else:
        print('Configuring ' + devicename + ' as a VTP Client ')
        config_commands = ['vtp mode client', vtp_domain_command]
        output = myssh.send_config_set(config_commands)
        print(output)
