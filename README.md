# SecureAP Onboarding certfincate t_renewal
Secure AP onbarding is feature on SDA released as part of the 2.3.3 release, This feature allows the AP to enable dot1x supplicant and start authentication with the upstream fabric edge.If the AP is enbaled for EAP-TLS a certificate is issued to the AP as part of the PnP process and the certificate has a expiry time as defined on the Cisco Catalyst center. For the AP do a certficate renewal the AP needs be rebooted once the certificate expiry happens. Once reloaded the AP will again go back to factory default and get a news certificate from the Cisco Catalyst Center. The disadvantage with this approach is that one would need to wait till the expiry time to occur for the AP to receive the new certificate.
For customers who would want to renew the cert in advance we have an python script that runs  on guest shell within the cisco catayst 9800 wireless lan contreoller. the python script is invoked with cron entry based on the cron entry which will validate the current time and expiry time of the AP. If the difference is between the expiry time and current time is less than or equal to the user defined time. The script would go ahead and issue a factory reset of the AP to start the onboading workflow so that a new certificte is issued by the Cisco catalyst centre.

##pre-requiste
  -Cisco 9800 Wireless LAN controller
  -App hosting enabled on C9800 WLAN controller
  -Guest shell enabled 
For more information on how to enable guest shell on the C9800 wireless LAN controller. Refer the following URL
[Guest Shell on IOS XE platforms](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/173/b_173_programmability_cg/guest_shell.html)

