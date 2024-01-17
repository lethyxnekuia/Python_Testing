import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    list_clubs = [club for club in clubs
                  if club['email'] == request.form['email']]
    if list_clubs:
        return render_template(
            'welcome.html',
            club=list_clubs[0],
            competitions=competitions
        )
    return render_template('index.html', email_not_found=True), 404


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html',
            club=foundClub,
            competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions
                   if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    availablePoints = int(club.get('points', None))
    competitionDate = datetime.strptime(
        competition.get('date', None), "%Y-%m-%d %H:%M:%S")
    if placesRequired > availablePoints:
        message = "You have not enough points."
        flash(message, 'error')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )
    if placesRequired > 12:
        message = "You can not book more than 12 places"
        flash(message, 'error')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )
    if competitionDate < datetime.now():
        message = "This event has passed"
        flash(message, 'error')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )

    for compet in competitions:
        if compet['name'] == competition['name']:
            compet['numberOfPlaces'] = int(
                compet['numberOfPlaces']) - placesRequired
    competitions_dict = {
        "competitions": competitions
    }
    with open("competitions.json", "w") as outfile:
        json.dump(competitions_dict, outfile)

    for cl in clubs:
        if cl['name'] == club['name']:
            cl["points"] = int(club["points"]) - placesRequired
    clubs_dict = {
        "clubs": clubs
    }
    with open("clubs.json", "w") as outfile:
        json.dump(clubs_dict, outfile)

    flash('Great-booking complete!')
    return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )


@app.route('/clubsPoints')
def clubsPoints():
    return render_template('clubs_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
