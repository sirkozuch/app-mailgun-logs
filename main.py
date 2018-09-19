import requests
import datetime
import pandas as pd
from pandas.io.json import json_normalize
from keboola import docker



par = docker.Config('/data/').get_parameters()

mailing_list    =   par['mailing_list']
user            =   par['user']
token           =   par['#token']
url             =   par['url']
start           =   (datetime.datetime.today() - \
                    datetime.timedelta(days=1)).strftime\
                    ('%a, %d %b %Y %H:%M:%S') + ' +0000'

try:
    subject     =   par['subject']
except:
    subject     =   None


mailing_list_path   =   '/data/in/tables/' + mailing_list
data                =   pd.read_csv(mailing_list_path)

def get_logs(recipient, user, token, subject, begin="Mon, 01 Jan 2018 00:00:00 +0000"):
    return requests.get(
        url,
        auth=(user, token),
        params={"begin"       : begin,
                "ascending"   : "yes",
                "subject"     : subject,
                "limit"       : 25,
                "pretty"      : "yes",
                "recipient"   : recipient
                })


event = []
event_dates = []

for index, row in data.iterrows():
    recipient = row['email']

    res = get_logs(recipient, 
                   user, 
                   token, 
                   subject, 
                   start).json()['items']

    log = json_normalize(res)

    if log.shape[0] != 0:
        log['date'] = [datetime.date.fromtimestamp(x['timestamp'])
                    for x in res]
        print('Some logs fetched for %s' % recipient)

        if "delivered" in log.event.unique():
            event += ['delivered']
            event_dates += [log.date.max().strftime('%Y-%m-%d')]
        elif "accepted" in log.event.unique():
            event += ['accepted']
            event_dates += [log.date.max().strftime('%Y-%m-%d')]
        else:
            event += ['']
            event_dates += ['']
    else:
        event += ['']
        event_dates += ['']
        print('No logs fetched for %s' % recipient)

data['event'] = event
data['date']  = event_dates

data.to_csv('/data/out/tables/logs.csv', index=False)













