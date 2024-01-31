# Introduction
Secure AP onboarding is a featured capability introduced in SDA as part of the 2.3.3 release. This functionality empowers the Access Point (AP) to activate the dot1x supplicant, initiating authentication with the upstream fabric edge. When the AP is configured for EAP-TLS, a certificate is seamlessly issued during the Plug and Play (PnP) process. This certificate possesses a defined expiration time as set in the Cisco Catalyst Center.

To facilitate AP certificate renewal, a reboot is necessitated upon certificate expiry. Post-reboot, the AP reverts to factory defaults, triggering the acquisition of a new certificate from the Cisco Catalyst Center. A limitation of this method is the obligatory wait until the certificate's expiration for the issuance of a new one.

For proactive certificate renewal, we offer a Python script running within the guest shell of the Cisco Catalyst 9800 wireless LAN controller. The script is scheduled via a cron entry, enabling validation of the current time against the AP's certificate expiration. If the time difference falls within the user-defined threshold, the script initiates a factory reset of the AP. This restarts the onboarding workflow, facilitating the issuance of a new certificate by the Cisco Catalyst Center


## Pre-requisite
  - Cisco 9800 Wireless LAN controller
  - App hosting enabled on C9800 WLAN controller
  - Guest shell enabled 
For more information on how to enable guest shell on the C9800 wireless LAN controller.
[Guest Shell on IOS XE platforms](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/173/b_173_programmability_cg/guest_shell.html)

## Enabling Guestshell and running the Python script

Configurations to enable Guest shell on the C9800

```
app-hosting appid guestshell
 app-vnic management guest-interface 3
 app-default-gateway 192.168.1.1 guest-interface 3
```
Verify app-hosting is enabled
```
show iox
IOx Infrastructure Summary:
---------------------------
IOx service (CAF)              : Running
IOx service (HA)               : Running
IOx service (IOxman)           : Running
IOx service (Sec storage)      : Not Supported
Libvirtd 5.5.0                 : Running
Dockerd v19.03.13-ce           : Running
Redundancy Status              : Non-Redundant
Sync status                    : Standby unavailable
```

Enable Guest shell and verify
```
9800#show app-hosting list
App id                                   State
---------------------------------------------------------
guestshell                               RUNNING
```
Once Guestshell is enabled copy the Python code to the flash of the Wireless LAN Controller
```
9800-3#dir flash:guest-share
Directory of bootflash:/guest-share/

32390   -rw-             2002  Jan 30 2024 18:45:08 +00:00  ap_reboot.py
```
Invoke the script using EEM, and modify the cron entry as per the user's need.
```
event manager directory user policy "flash:/guest-share"
event manager applet check-ap-expiry
 event timer cron cron-entry "* * * * *"
 action 1.0 cli command "enable"
 action 2.0 syslog msg " Starting AP expiry check script"
 action 3.0 cli command "guestshell run python3 /flash/guest-share/ap_reboot.py -d  1"
```
To define the user threshold for the cert renewal add it as part of the argument to the script
```
guestshell run python3 /flash/guest-share/ap_reboot.py -d <no_of_days>
```

## Log File

the log file is generated whenever the script is executed and is placed in the flash.
```
9800-3#dir flash:guest-share
Directory of bootflash:/guest-share/

32386   -rw-            25701  Jan 30 2024 19:24:10 +00:00  ap_expiry_log.txt
```
sample output of the log file

```
9800-3#  more flash:guest-share/ap_expiry_log.txt
##################################################
2024-01-30 18:46:04.353958
Based on user input,AP with cert expire time of less than 1 days will be rebooted

Config not cleared for sand3800-fusion-te-1-0-3 since expiry diff is 866 days
Config not cleared for sand-3800-fe2-gi-1-0-7 since expiry diff is 868 days
Config not cleared for RAP_sda_1 since expiry diff is 1931 days
Config not cleared for 9130-RAP since expiry diff is 27585 days
Config not cleared for APC4B2.39BD.9CAC since expiry diff is 1931 days
Config not cleared for sand-4800-9300-fe1-1-0-3 since expiry diff is 1931 days
Config not cleared for map_sda_1 since expiry diff is 1931 days
```

