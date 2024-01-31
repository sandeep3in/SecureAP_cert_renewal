import argparse
import re
from cli import cli
from datetime import datetime
import eem
import time
import sys


def ap_reload(ap_dct,time):
    #unpack dict to get the AP name(k) and expiry date(v)
    for k,v in ap_dct.items():
        date_object = datetime.strptime(v, "%m/%d/%Y %H:%M:%S")
        # Get the current date and time
        current_time = datetime.now()

        # Calculate the difference between the two dates
        time_difference = date_object - current_time
        if time_difference.days<=time:
            cli("clear ap config {}".format(k))
            print('Config cleared for {} Since expirt diff \
is {}\n'.format(k,time_difference.days))
        else:
            print('Config not cleared for {} since expiry diff is {} days\
'.format(k,time_difference.days))


old_stdout=sys.stdout
sys.stdout=open('/flash/guest-share/ap_expiry_log.txt', 'a+')
current_dateTime = datetime.now()
sys.stdout.write('\n')
sys.stdout.write('#'*50)
sys.stdout.write('\n')
sys.stdout.write(str(current_dateTime))
sys.stdout.write('\n')

ap_expiry_dct={}
    
#Create the parser for extracting the expiry time
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--days',type=int, required=True, help='specifcy the days any AP below threshhold would reboot')
args = parser.parse_args()

print ('Based on user input,AP with cert expire time of less than\
 {} days will be rebooted \n'.format(args.days))

# get the AP list from the WLC
ap_summ=cli("show ap summary")
ap_list= re.findall('(^\S+)\s+\d+',ap_summ,re.MULTILINE)

#extract the expiry date of the certificate 
for i in ap_list:
    ap_expiry_1=cli("sh ap name {}  config general | in Expi".format(i))
    try:
        ap_expiry=re.search('^(.*):\s+(.*)\n',ap_expiry_1)
        ap_expiry_dct[i]=ap_expiry.group(2)
        #print('the expiry time for {}:  {}\n'.format(i,ap_expiry))
    except:
        print('failed to extract the expiry time for {}'.format(i))


ap_reload(ap_expiry_dct,args.days)
    
