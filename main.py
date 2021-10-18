from flask import Flask, render_template, request, redirect
from player_search import check_name
from evaluate import evaluate
import pandas as pd
from metrics import power_rankings

app = Flask(__name__)

ped = pd.read_csv('static/players_events_17102021.csv')
players = []

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/playercomp')
def playercomp():
  players.clear()
  return render_template('playercomp.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/p1_init')
def p1_init():
  return render_template('p1_init.html')

@app.route('/p1_choice', methods = ["POST"])
def p1_choice():
  p1_namepart = request.form.get('p1_name_try')
  global division
  division = request.form.get('division')

  if not p1_namepart or division == 'Division':
    error_message = 'Please enter at least one letter and choose a division.'
    return render_template('p1_init.html', error_message = error_message, p1_namepart=p1_namepart)

  global results1
  results1 = check_name(p1_namepart, division, ped)

  if len(results1) == 0:
    error_message = "We couldn't find anyone by that name. Please try again."
    return render_template('p1_init.html', error_message = error_message)

  if len(results1) > 15:
    error_message = "This search returned too many results. Please be more specific."
    return render_template('p1_init.html', error_message = error_message, p1_namepart=p1_namepart)

  return render_template('p1_choice.html', results1 = results1, division = division)

@app.route('/p2_init/<player1>')
def p2_init(player1):
  players.append(player1)
  return render_template('p2_init.html', player1 = player1, results1 = results1, division = division)

@app.route('/p2_choice', methods = ["POST"])
def p2_choice():
  p2_namepart = request.form.get('p2_name_try')

  if not p2_namepart:
    error_message = 'Please enter at least one letter and choose a division.'
    return render_template('p2_init.html', error_message = error_message, p2_namepart=p2_namepart)

  global results2
  results2 = check_name(p2_namepart, division, ped)

  if len(results2) == 0:
    error_message = "We couldn't find anyone by that name. Please try again."
    return render_template('p2_init.html', error_message = error_message)

  if len(results2) > 15:
    error_message = "This search returned too many results. Please be more specific."
    return render_template('p2_init.html', error_message = error_message, p2_namepart=p2_namepart)

  return render_template('p2_choice.html', results2 = results2)

@app.route('/options/<player2>')
def options(player2):
  if player2 != 'nope':
    players.append(player2)
  for result in results1:
    if int(result[4]) == int(players[0]):
      player_1_name = result[1]
  for result in results2:
    if int(result[4]) == int(players[1]):
      player_2_name = result[1]

  return render_template('options.html', player_1_name = player_1_name, player_2_name = player_2_name)



@app.route('/analysis', methods = ["POST"])
def analysis():
  for result in results1:
    if int(result[4]) == int(players[0]):
      player_1_name = result[1]
  for result in results2:
    if int(result[4]) == int(players[1]):
      player_2_name = result[1]

  tourneys = request.form.get('tourneys')
  years = request.form.get('years')

  final_results = evaluate(players, tourneys, years, ped)
  
  return render_template('analysis.html', player_1_name=player_1_name, player_2_name=player_2_name, final_results=final_results)

@app.route('/metrics', methods = ["GET", "POST"])
def metrics():
  power_tups = None
  metric_type = None
  metric_division = None
  if request.method == 'POST':
    metric_type = request.form.get('metric')
    metric_division = request.form.get('division')
    if metric_type == 'Power':
      power_tups = power_rankings(metric_division, ped)
    
  
  return render_template('metrics.html', metric_type = metric_type, metric_division = metric_division, power_tups = power_tups)


if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )