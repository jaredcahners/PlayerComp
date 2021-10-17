import csv
import pandas as pd

def evaluate(players, tourneys, years):
    tdict = {}
    with open('static/tournaments.csv', 'r') as csvfile:
        for row in csv.reader(csvfile):
            tdict[row[0]] = (row[1], row[3])
            
    results = []
    
    ped = pd.read_csv('static/ped_small.csv')
    
    players = [int(i) for i in players]
    
    for tn in tdict.keys():
        if ped[f'{tn}_place'][players[0]] == 0 and ped[f'{tn}_place'][players[1]] == 0:
            continue
        if tourneys == 'Both':
          if ped[f'{tn}_place'][players[0]] == 0 or ped[f'{tn}_place'][players[1]] == 0:
            continue

        if years != 'Allyears':
          if years != tdict[tn][1]:
            continue
        
        results.append((tdict[tn][0], ped[f'{tn}_place'][players[0]], ped[f'{tn}_place'][players[1]]))
        
    return results