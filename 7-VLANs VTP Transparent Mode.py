from netmiko import ConnectHandler

# Define the list of switch IP addresses
switch_ips = ['192.168.8.101', '192.168.8.102', '192.168.8.103']

# Iterate over each switch IP address
for ip in switch_ips:
    print('Configuring VLANs on ' + ip + '-' * 30)

    # Prompt for SSH username and password
    USER = input('SSH Username: ')
    PASS = input('SSH Password: ')

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

    # Prompt for VLAN configuration
    vlans = input('Enter the VLANs you would like to create [1 or 1,2,10 or 1-10]: ')
    print('Configuring ' + devicename + ' as a Transparent Switch with VLANs ' + vlans)

    # Construct VLAN configuration commands
    vlan_command = 'vlan ' + vlans
    vtp_domain_command = 'vtp domain cisco'  # Adding VTP domain command
    config_commands = [vtp_domain_command, 'vtp mode transparent', vlan_command]

    # Send configuration commands to the switch
    output = myssh.send_config_set(config_commands)
    print(output)
