API_URL = 'https://virtualapi.flapmyport.com/'
# URL of FlapMyPort API root
# Example: 'https://virtualapi.flapmyport.com/'

CHECK_INTERVAL = 5 * 60


EXEC_COMMAND = '/usr/local/bin/notify.sh --header="$short_text"'

# Command that called if new events detected.
# Example:
# '/usr/local/bin/notify.sh --header="$short_text"'
#
# Command can contain variables. Following variabled are available:
#
# $up_ports
#  Total number of ports that have been changing state and currently 'up'
#  Example: 1
#
# $down_ports
#  Total number of ports that have been changing state and currently 'down'
#  Example: 3
#
# $full_text
#  Textual summary of what happened for a period
#  Example:
#  Chicago-router1 xe-0/1/0 (ChicagoMusicExchange): up [1]
#  DALLAS-Switch1 FastEthernet0/0 (out-of-service): up [14]
#  core1.mynet.com xe-0/0/0 (core4): up [1]
#  core4.mynet.com xe-1/0/0 (core1): up [1]
#  EdgeRTR-1 xe-1/2/3 (Equinix): down [1]
#  Chicago-router2 fxp0 (Mgmt): up [2]
#
# $short_text
#  Textual short summary what happend for a period
#  Examples:
#  'Chicago-router1: xe-0/0/5 down [1]'
#  '2 ports down, 5 up on 6 hosts'
#
# $flap_count
#  Total number of flaps of all ports of all devices for a period
#  Example: 20
#
# $affected_devices:
#  Number of unique hosts affected for a period.
#  Example: 6
