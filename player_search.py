import pandas as pd
import re

ped = pd.read_csv('static/players_events_17102021.csv')

def check_name(namepart, division_in):
    '''
    Given a possible name or part of a name, returns a list of tuples for possible matches.
    '''
    fulllist = []
    for ind, row in ped.iterrows():
        namepile = row['name'].replace(" ", "").lower()
        fulllist.append((namepile, row['name'], row['division'], row['id'], ind))
    dups = []
    for n in fulllist:
        np = n[0]
        division = n[2]
        if re.match('[a-zA-Z \-\']*{}[a-zA-Z \-\']*'.format(namepart.replace(" ","").lower()), np) and division == division_in:
            dups.append(n)
    return dups