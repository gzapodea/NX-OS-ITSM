

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import service_now_apis
import time
import requests
import os
os.chdir("/bootflash/NX-OS-ITSM")

from cli import cli

from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


# syslog entry that triggered the event
syslog_info = "%ETHPORT-5-IF_DOWN_CFG_CHANGE: Interface Ethernet1/1 is down"


# retrieve the device hostname
device_name = cli("show run | in hostname")

location = "NYC, floor 3"

# define the incident description and comment
short_description = "Nexus Switch Uplink Down - NX OS Automation"
comment = "The Nexus switch with the " + device_name + "\n has detected an Uplink Interface Down"
comment += "\n\nThe device location is " + location
comment += "\n\nSyslog: " + syslog_info


# create a new ServiceNow incident
incident = service_now_apis.create_incident(short_description, comment, SNOW_DEV, 3)


# write the new incident name to file in /bootflash/PCW
incident_file = open("/bootflash/NX-OS-ITSM/uplink_ticket.txt", "w")
incident_file.write(incident)
incident_file.close()


print("End Application Run Uplink Interface Down")
