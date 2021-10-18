def power_rankings(div, ped):
  pr_tups = []
  pr_df = ped[ped['division'] == div].sort_values('power_ranking', ascending = False).head(30)
  n=1
  for ind, row in pr_df.iterrows():
    pr_tups.append((n, row['name'], row['events_played'], row['power_ranking']))
    n+=1
  return pr_tups