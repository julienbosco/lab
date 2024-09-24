#!/bin/vbash
source /opt/vyatta/etc/functions/script-template
configure
set interfaces ethernet eth0 description AIRGAPPED
set interfaces ethernet eth0 address 10.243.99.1/24

set service dhcp-server shared-network-name TGE subnet 10.243.99.0/24 option default-router '10.243.99.1'
set service dhcp-server shared-network-name TGE subnet 10.243.99.0/24 option name-server '10.243.99.1'
set service dhcp-server shared-network-name TGE subnet 10.243.99.0/24 lease '86400'
set service dhcp-server shared-network-name TGE subnet 10.243.99.0/24 range 0 start '10.243.99.20'
set service dhcp-server shared-network-name TGE subnet 10.243.99.0/24 range 0 stop '10.243.99.200'
set service dhcp-server shared-network-name TGE subnet 10.243.99.0/24 subnet-id '1'

set service dns forwarding listen-address '10.243.99.1'
set service dns forwarding allow-from '10.243.99.0/24'
set service dns forwarding cache-size '0'

set interfaces ethernet eth1 description DMZ
set interfaces ethernet eth1 address 10.243.1.2/24

set firewall global-options state-policy established action accept
set firewall global-options state-policy related action accept
set firewall global-options state-policy invalid action drop

set firewall zone TGE interface eth0
set firewall zone TGE description 'Zone AIRGAPPED'
set firewall zone DMZ interface eth1
set firewall zone DMZ description 'Zone DMZ (connectée à Cegep-DMZ)'
set firewall zone LOCAL local-zone
set firewall zone LOCAL description 'Le routeur'

set firewall zone TGE default-action drop
set firewall zone DMZ default-action drop
set firewall zone LOCAL default-action drop

set firewall zone DMZ from TGE firewall name TGEv4-to-DMZv4
set firewall zone DMZ from LOCAL firewall name LOCALv4-to-DMZv4
set firewall zone TGE from DMZ firewall name DMZv4-to-TGEv4
set firewall zone TGE from LOCAL firewall name LOCALv4-to-TGEv4 
set firewall zone LOCAL from TGE firewall name TGEv4-to-LOCALv4
set firewall zone LOCAL from DMZ firewall name DMZv4-to-LOCALv4

set firewall ipv4 name TGEv4-to-DMZv4 default-action drop
set firewall ipv4 name TGEv4-to-DMZv4 rule 1 destination address 10.243.1.0/24
set firewall ipv4 name TGEv4-to-DMZv4 rule 1 action accept

set firewall ipv4 name DMZv4-to-TGEv4 default-action drop
set firewall ipv4 name DMZv4-to-TGEv4 rule 1 source address 10.243.1.0/24
set firewall ipv4 name DMZv4-to-TGEv4 rule 1 action accept

set firewall ipv4 name DMZv4-to-LOCALv4 default-action drop
set firewall ipv4 name DMZv4-to-LOCALv4 rule 1 action accept
set firewall ipv4 name DMZv4-to-LOCALv4 rule 1 destination port 22
set firewall ipv4 name DMZv4-to-LOCALv4 rule 1 destination address 10.243.1.1


