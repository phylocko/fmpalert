# What is FMPAlarm?

This is a notification mechanism for [FlapMyPort](https://flapmyport.com) monitoring system.

# What it actually does
- Asks FlapMyPort API every period of time about new events
- Prepares textual representation of the events
- Calls a custom script if event list is not empty

# What do you need to deploy it
- [flapmyport_api](https://github.com/phylocko/flapmyport_api) set up and running

# Quick start #

### 1. Create and set a python virtual env
```
virtualenv ~/env/fmpalarm
source ~/env/fmpalarm/bin/activate
pip install -r requirements.txt
```

### 2. Edit a config file

**settings.py:**
```
# URL of your FlapMyPort API
API_URL = 'https://virtualapi.flapmyport.com/'

# Which command to call if events are found
EXEC_COMMAND = '/usr/local/bin/notify.sh --header="$short_text"'
```

_You can use pre-defined variables to customize your command. See list of the available variabled below._

### 3. Test the FMPAlarm script
```
python3 notify.sh
```

### 4. Enable loading the FMPAlert via systemd

Use the `fmpalert.service` file that are located in the distribution.

# List of the available variables

### $up_ports
Total number of ports that have been changing state and currently 'up'.

Example: `1`

### $down_ports

Total number of ports that have been changing state and currently 'down'

Example:`3`

### $full_text
Textual summary of what happened for a period

Example:
```
Chicago-router1 xe-0/1/0 (ChicagoMusicExchange): up [1]
DALLAS-Switch1 FastEthernet0/0 (out-of-service): up [14]
core1.mynet.com xe-0/0/0 (core4): up [1]
core4.mynet.com xe-1/0/0 (core1): up [1]
EdgeRTR-1 xe-1/2/3 (Equinix): down [1]
Chicago-router2 fxp0 (Mgmt): up [2]
```

### $short_text
Textual short summary what happend for a period

Examples:

`Chicago-router1: xe-0/0/5 down [1]`

`2 ports down, 5 up on 6 hosts`

### $flap_count

Total number of flaps of all ports of all devices for a period

Example: `20`

### $affected_devices:

Number of unique hosts affected for a period.

Example: `6`


---
*And may a stable network be with you!*