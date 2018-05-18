

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import requests
import service_now_apis
import time
import os
os.chdir("/bootflash/NX-OS-ITSM")

from cli import cli

from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


# the syslog entry that triggered the event
syslog_info = "%ETHPORT-5-IF_ADMIN_UP: Interface Ethernet1/1 is up"


# retrieve the device hostname
device_name = cli("show run | in hostname")


# define the incident description and comment
update_comment = "The Nexus switch with the " + device_name + "\n has recovered from the Uplink failure"
update_comment += "\n\nSyslog: " + syslog_info


# find the ServiceNow incident
file = open("uplink_ticket.txt", "r")
incident = file.read()
file.close()


# update the ServiceNow incident
service_now_apis.update_incident(incident, update_comment, SNOW_DEV)


# close ServiceNow incident
time.sleep(1)
service_now_apis.close_incident(incident, SNOW_DEV)


# delete the incident name from the file in /bootflash/PCW
incident_file = open("/bootflash/NX-OS-ITSM/uplink_ticket.txt", "w")
incident_file.write("INCIDENT")
incident_file.close()



print("End Application Run Uplink Interface Restored")
