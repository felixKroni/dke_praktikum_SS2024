import datetime
from urllib.parse import urlsplit

import requests
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from sqlalchemy.orm import joinedload

from app import app, database
from app.forms.fahrplanForm import SpecificDateForm, \
    WeeklyDaysForm, ConfirmFahrplanForm, FahrplanForm
from app.forms.halteplanCreateForm import HalteplanCreateForm, HalteplanChooseHaltepunktForm, HalteplanChoosePricesForm
from app.forms.halteplanEditForm import HalteplanEditForm
from app.forms.loginForm import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

from app.forms.mitarbeiterEditForm import MitarbeiterEditForm
from app.forms.mitarbeiterRegistrationForm import MitarbeiterRegistrationForm
from app.models.abschnitt import Abschnitt
from app.models.abschnitt_halteplan import AbschnittHalteplan
from app.models.fahrdurchfuehrung import Fahrtdurchfuehrung
from app.models.fahrplan import Fahrplan
from app.models.halteplan import Halteplan
from app.models.mitarbeiter import Mitarbeiter


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = database.get_controller('ma').get_mitarbeiter_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Falscher Benutzername oder Passwort')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registerMitarbeiter', methods=['GET', 'POST'])
@login_required
def registerMitarbeiter():
    # if current_user.is_authenticated:
    #    return redirect(url_for('index'))
    form = MitarbeiterRegistrationForm()
    if form.validate_on_submit():
        user = Mitarbeiter(username=form.username.data, email=form.email.data, svnr=form.svnr.data, name=form.name.data,
                           role=form.role.data)
        user.set_password(form.password.data)
        database.baseController.add(user)
        # database.Session.commit()
        flash('Mitarbeiter ' + user.username + ' wurde erfolgreich erstellt')
        return redirect(url_for('mitarbeiterList'))
    return render_template('registerMitarbeiter.html', title='Register', form=form)


@app.route('/mitarbeiterList', methods=['GET'])
@login_required
def mitarbeiterList():
    if current_user.is_authenticated:
        return render_template('mitarbeiterList.html', title='Mitarbeiter',
                               mitarbeiters=database.baseController.find_all(Mitarbeiter))
    return redirect(url_for('index'))


@app.route('/deleteMitarbeiter/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteMitarbeiter(id):
    if current_user.is_authenticated:
        user = database.baseController.find_by_id(Mitarbeiter, id)
        if user is not None:
            database.baseController.delete(user)
            flash('Mitarbeiter erfolgreich gelöscht')
        return redirect(url_for('mitarbeiterList'))
    return redirect(url_for('index'))


@app.route('/editMitarbeiter/<int:id>', methods=['GET', 'POST'])
@login_required
def editMitarbeiter(id):
    if current_user.is_authenticated:
        user = database.baseController.find_by_id(Mitarbeiter, id)
        if user is not None:
            if request.method == 'GET':
                form = MitarbeiterEditForm()
                form.username.data = user.username
                form.email.data = user.email
                form.svnr.data = user.svnr
                form.name.data = user.name
                form.role.data = user.role
                form.submit.label.text = 'Update'
            else:
                form = MitarbeiterEditForm(request.form)
                if form.validate_on_submit():
                    user.username = form.username.data
                    user.email = form.email.data
                    user.svnr = form.svnr.data
                    user.name = form.name.data
                    user.role = form.role.data
                    user.set_password(form.password.data)
                    database.baseController.update_by_id(Mitarbeiter, user.id, user.__dict__)
                    flash('Mitarbeiter erfolgreich geändert')
                return redirect(url_for('mitarbeiterList'))

            return render_template('editMitarbeiter.html', title='Edit', form=form)
        else:
            flash('Kein Mitarbeiter mit dieser ID gefunden ' + id)
        return redirect(url_for('mitarbeiterList'))
    return redirect(url_for('index'))


# Halteplan routes
@app.route('/halteplanList', methods=['GET'])
@login_required
def halteplanList():
    halteplaene = database.baseController.find_all(Halteplan)
    return render_template('halteplanList.html', title='Haltepläne', halteplaene=halteplaene)


@app.route('/createHalteplan', methods=['GET', 'POST'])
@login_required
def createHalteplan():

    form = HalteplanCreateForm(request.form)
    form.streckenName.choices = get_strecken()
    if form.validate_on_submit():
        session['form_data'] = {
            'name': form.name.data,
            'streckenName': form.streckenName.data
        }
        #new_halteplan = Halteplan(name=form.name.data, streckenName=form.streckenName.data)
        #database.baseController.add(new_halteplan)
        #flash('Erfolgreich neuen Halteplan erstellt')
        return redirect(url_for('chooseHaltestellen'))
    return render_template('createHalteplan.html', title='Halteplan erstellen', form=form)

@app.route('/chooseHaltestellen', methods=['GET', 'POST'])
@login_required
def chooseHaltestellen():
    form_data = session.get('form_data', {})
    form = HalteplanChooseHaltepunktForm(request.form)
    selectedStrecke = form_data.get('streckenName')
    halteplanName = form_data.get('name')
    form.haltepunkte.choices = get_haltepunkte_names(selectedStrecke)
    if form.validate_on_submit():
        halteplan = Halteplan(name=halteplanName, streckenName=selectedStrecke)
        halteplan = database.baseController.add(halteplan)

        haltepunkte = form.haltepunkte.data
        for i in range(len(haltepunkte) - 1):
            start_bahnhof = haltepunkte[i]
            end_bahnhof = haltepunkte[i + 1]
            create_abschnitt(start_bahnhof, end_bahnhof, selectedStrecke, halteplan.id, i)

        return redirect(url_for('choosePrices', halteplan_id=halteplan.id))
    return render_template('chooseHaltestellen.html', title='Haltestellen auswählen', form=form)


@app.route('/choosePrices/<int:halteplan_id>', methods=['GET', 'POST'])
@login_required
def choosePrices(halteplan_id):
    form = HalteplanChoosePricesForm(request.form)
    abschnitte = database.get_controller('hp').get_abschnitte(halteplan_id)
    if form.validate_on_submit():
        for abschnitt in abschnitte:
            nutzungsentgelt = request.form.get('nutzungsentgelt_' + str(abschnitt.id))
            if nutzungsentgelt:
                # Update logic here
                abschnitt.nutzungsentgelt = float(nutzungsentgelt)
                database.baseController.update_by_id(Abschnitt, abschnitt.id, abschnitt.__dict__)
                # Save to database
        flash('Preise erfolgreich aktualisiert.')
        return redirect(url_for('halteplanList'))

    form.abschnitte = abschnitte
    return render_template('choosePrices.html', title='Preise festlegen', form=form)


@app.route('/editHalteplan/<int:id>', methods=['GET', 'POST'])
@login_required
def editHalteplan(id):
    halteplan = database.baseController.find_by_id(Halteplan, id)
    if halteplan is not None:
        form = HalteplanEditForm(request.form)
        form.halteplan_id = id
        strecken_list = get_strecken()
        form.streckenName.choices = strecken_list
        form.haltepunkte.choices = get_haltepunkte_names(halteplan.streckenName)
        if request.method == 'GET':
            form.name.data = halteplan.name
            form.streckenName.data = halteplan.streckenName
            haltepunkte = []
            for abschnitt_halteplan in halteplan.abschnitte:
                abschnitt = database.baseController.find_by_id(Abschnitt, abschnitt_halteplan.abschnitt_id)
                haltepunkte.append(abschnitt.StartBahnhof)
                haltepunkte.append(abschnitt.EndBahnhof)
            #Remove duplicates
            haltepunkte = list(set(haltepunkte))
            form.haltepunkte.data = haltepunkte
        elif form.validate_on_submit():
            halteplan.name = form.name.data
            halteplan.streckenName = form.streckenName.data

            #remove existing abschnitte
            database.get_controller('hp').delete_abschnitt_relations(halteplan.id)

            #insert the new ones
            haltepunkte = form.haltepunkte.data
            for i in range(len(haltepunkte) - 1):
                start_bahnhof = haltepunkte[i]
                end_bahnhof = haltepunkte[i + 1]
                create_abschnitt(start_bahnhof, end_bahnhof, halteplan.streckenName , halteplan.id, i)


            database.baseController.update_by_id(Halteplan, id, halteplan.__dict__)

            flash('Halteplan erfolgreich geändert')
            return redirect(url_for('halteplanList'))
        return render_template('editHalteplan.html', form=form, title='Edit Halteplan')
    else:
        flash('No Halteplan found with ID: {}'.format(id))
        return redirect(url_for('halteplanList'))


@app.route('/deleteHalteplan/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteHalteplan(id):
    halteplan = database.baseController.find_by_id(Halteplan, id)
    if halteplan is not None:
        #TODO delete all accordinng Fahrpläne and Fahrtdurchführungen
        database.get_controller('hp').delete_abschnitt_relations_with_halteplan(halteplan.id)
        flash('Halteplan gelöscht')
    else:
        flash('Kein Halteplan wurde mit dieser ID gefunden: {}'.format(id))
    return redirect(url_for('halteplanList'))




@app.route('/createFahrplan', methods=['GET', 'POST'])
@login_required
def createFahrplan():
    form = FahrplanForm(request.form)
    data = database.baseController.find_all(Halteplan)
    form.halteplan_selection.choices = [(halteplan.id, halteplan.name + ' - ' + halteplan.streckenName) for halteplan in data]

    if form.validate_on_submit():
        name = form.name.data
        gueltig_von = form.gueltig_von.data
        gueltig_bis = form.gueltig_bis.data
        selected_halteplan_id = form.halteplan_selection.data
        hp = database.baseController.find_by_id(Halteplan, selected_halteplan_id)
        new_fahrplan = Fahrplan(name=name, gueltig_von=gueltig_von, gueltig_bis=gueltig_bis, halteplan=hp,
                                halteplan_id=hp.id)
        new_fahrplan = database.baseController.add(new_fahrplan)


        choice = form.choice.data
        if choice == 'specific':
            return redirect(url_for('specificDates', fahrplanId=new_fahrplan.id))
        elif choice == 'weekly':
            return redirect(url_for('weeklyDays', fahrplanId=new_fahrplan.id))
    return render_template('createFahrplan.html', title='Fahrplan erstellen', form=form)


@app.route('/specificDates/<int:fahrplanId>', methods=['GET', 'POST'])
@login_required
def specificDates(fahrplanId):
    form = SpecificDateForm()
    if form.validate_on_submit():
        # Save specific dates and times to session or process as needed
        return redirect(url_for('confirmFahrplan'))
    return render_template('specificDates.html', form=form)

@app.route('/weeklyDays/<int:fahrplanId>', methods=['GET', 'POST'])
@login_required
def weeklyDays(fahrplanId):
    form = WeeklyDaysForm(request.form)
    if form.validate_on_submit():
        # TODO Züge aus Zugsystem nehmen
        fahrplan = database.baseController.find_by_id(Fahrplan, fahrplanId)
        if fahrplan is not None:
            weekday = form.weekdays.data
            time = form.time.data
            fahrplan_startDate = fahrplan.gueltig_von
            fahrplan_endDate = fahrplan.gueltig_bis
            #fahrplan_startDate = datetime.datetime.combine(startZeit, datetime.time())
            fahrplan_endDate = fahrplan_endDate.replace(hour=23, minute=59, second=59)
            start_time = time['start_time']
            end_time = time['end_time']


            startZeit = get_date_of_next_weekday(fahrplan_startDate, weekday)
            startZeit = datetime.datetime.combine(startZeit, datetime.time()) # convert to datetime object
            startZeit = startZeit.replace(hour=time['start_time'].hour, minute=time['start_time'].minute)
            print('Erster Tag: '+str(startZeit))

            while startZeit <= fahrplan_endDate:
                if startZeit.weekday() == weekday_converter(weekday):
                    if start_time <= startZeit.time() <= end_time:
                        print(startZeit)
                        new_fahrtdurchfuehrung = Fahrtdurchfuehrung(fahrplan_id=fahrplanId, startZeit=startZeit, ausfall=False, verspaetung=False, )
                        database.baseController.add(new_fahrtdurchfuehrung)
                    startZeit += datetime.timedelta(hours=int(time['interval']))
                else:
                    print('Nicht der richtige Wochentag: ' + str(startZeit))
                    print('Suche neuen Wochentag')
                    startZeit = get_date_of_next_weekday(startZeit, weekday)
                    startZeit = datetime.datetime.combine(startZeit, datetime.time())  # convert to datetime object
                    startZeit = startZeit.replace(hour=time['start_time'].hour, minute=time['start_time'].minute)



                pass

            pass

        if 'new' in request.form:
            # Save the current time and add a new time input field
            return redirect(url_for('weeklyDays', fahrplanId=fahrplanId))
        return redirect(url_for('confirmFahrplan', fahrplanId=fahrplanId))
    else:
        print(form.errors)
    return render_template('weeklyDays.html', form=form)

@app.route('/confirmFahrplan/<int:fahrplanId>', methods=['GET', 'POST'])
@login_required
def confirmFahrplan(fahrplanId):
    form = ConfirmFahrplanForm()
    fahrplan = database.baseController.find_by_id(Fahrplan, fahrplanId)
    if fahrplan is not None:
        form.fahrplan = fahrplan
    if form.validate_on_submit():

        flash('Fahrplan successfully created!')
        return redirect(url_for('index'))
    return render_template('confirmFahrplan.html', form=form)


@app.route('/fahrplanList', methods=['GET'])
@login_required
def fahrplanList():
    fahrplaene = database.baseController.find_all(Fahrplan)
    return render_template('fahrplanList.html', title='Fahrpläne', fahrplaene=fahrplaene)


@app.route('/deleteFahrplan/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteFahrplan(id):
    pass


@app.route('/editFahrplan/<int:id>', methods=['GET', 'POST'])
@login_required
def editFahrplan(id):
    pass


@app.route('/fahrtdurchfuehrungList', methods=['GET'])
@login_required
def fahrtdurchfuehrungList():
    fahrplaene = database.baseController.find_all(Fahrplan)
    return render_template('fahrtdurchfuehrungList.html', title='Fahrtdurchführungen', fahrplaene=fahrplaene)


@app.route('/deleteFahrtdurchfuehrung/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteFahrtdurchfuehrung(id):
    pass


@app.route('/editFahrtdurchfuehrung/<int:id>', methods=['GET', 'POST'])
@login_required
def editFahrtdurchfuehrung(id):
    pass




###########################
# REST requests
def get_strecken():
    response = requests.get("http://127.0.0.1:5001/api/strecken")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_all_haltepunkte_of_strecke(strecke_name):
    response = requests.get("http://127.0.0.1:5001/api/strecken/" + str(strecke_name))
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_haltepunkte_names(strecke_name):
    response = requests.get("http://127.0.0.1:5001/api/strecken/" + str(strecke_name))
    if response.status_code == 200:
        abschnitte = response.json().get('abschnitte', [])
        names = [abschnitt['startbahnhof_id'] for abschnitt in abschnitte]
        names.append(abschnitte[-1]['endbahnhof_id'])
        return names
    else:
        return None

# API´s
@app.route('/api/all_halteplaen_data', methods=['GET'])
def all_halteplaen_data():
    halteplaene = database.Session.query(Halteplan).options(
        joinedload(Halteplan.abschnitte).joinedload(AbschnittHalteplan.abschnitt),
        joinedload(Halteplan.fahrplan).joinedload(Fahrplan.fahrtdurchfuehrungen)
    ).all()

    result = []
    for halteplan in halteplaene:
        result.append(serialize_halteplan(halteplan))

    return jsonify({'halteplaene': result})





#####
# db functions


#create abschnitt by combining start and end bahnhof
def create_abschnitt(start_bahnhof, end_bahnhof, strecke_name, halteplan_id, reihung):
    start_bahnhof = str(start_bahnhof)
    end_bahnhof = str(end_bahnhof)
    strecke_name = str(strecke_name)
    all_abschnitte = get_all_haltepunkte_of_strecke(strecke_name)

    total_nutzungsentgelt = 0
    is_between = False
    all_abschnitte = all_abschnitte['abschnitte']
    for abschnitt in all_abschnitte:
        if abschnitt['startbahnhof_id'] == start_bahnhof and is_between is False:
            is_between = True
            total_nutzungsentgelt += abschnitt['nutzungsentgelt']
            if abschnitt['endbahnhof_id'] == end_bahnhof:
                break

        elif abschnitt['endbahnhof_id'] == end_bahnhof and is_between is True:
            total_nutzungsentgelt += abschnitt['nutzungsentgelt']
            is_between = False
            break

        elif is_between is True:
            total_nutzungsentgelt += abschnitt['nutzungsentgelt']

    new_abschnitt = Abschnitt(spurenweite=500, #TODO richtige werte ermitteln für spurenbreite
                              nutzungsentgelt=total_nutzungsentgelt, StartBahnhof=start_bahnhof, EndBahnhof=end_bahnhof)

    new_abschnitt = database.baseController.add(new_abschnitt)


    halteplan = database.baseController.find_by_id(Halteplan, halteplan_id)

    new_abschnitt_halteplan = AbschnittHalteplan(abschnitt_id=new_abschnitt.id, halteplan_id=halteplan.id, reihung=reihung)
    database.baseController.add(new_abschnitt_halteplan)

    database.baseController.commit()


def get_date_of_next_weekday(start_date, weekday):
    # Convert the weekday name to a weekday number
    target_weekday = weekday_converter(weekday)

    # Get the weekday number for the start date
    start_weekday = start_date.weekday()

    # Calculate how many days to add to get the next occurrence of the target weekday
    days_ahead = target_weekday - start_weekday
    if days_ahead < 0:
        days_ahead += 7

    # Calculate the next occurrence date by adding the calculated days to the start date
    next_occurrence_date = start_date + datetime.timedelta(days=days_ahead)

    return next_occurrence_date


def weekday_converter(weekday):
    return {
        'montag': 0,
        'dienstag': 1,
        'mittwoch': 2,
        'donnerstag': 3,
        'freitag': 4,
        'samstag': 5,
        'sonntag': 6
    }.get(weekday, 99)


def serialize_halteplan(halteplan):
    return {
        'id': halteplan.id,
        'name': halteplan.name,
        'streckenName': halteplan.streckenName,
        'abschnitte': [serialize_abschnitt_halteplan(ah) for ah in halteplan.abschnitte],
        'fahrplan': serialize_fahrplan(halteplan.fahrplan) if halteplan.fahrplan else None
    }


def serialize_abschnitt_halteplan(abschnitt_halteplan):
    return {
        'abschnitt_id': abschnitt_halteplan.abschnitt_id,
        'halteplan_id': abschnitt_halteplan.halteplan_id,
        'reihung': abschnitt_halteplan.reihung,
        'abschnitt': serialize_abschnitt(abschnitt_halteplan.abschnitt)
    }


def serialize_abschnitt(abschnitt):
    return {
        'id': abschnitt.id,
        'spurenweite': abschnitt.spurenweite,
        'nutzungsentgelt': abschnitt.nutzungsentgelt,
        'StartBahnhof': abschnitt.StartBahnhof,
        'EndBahnhof': abschnitt.EndBahnhof
    }


def serialize_fahrplan(fahrplan):
    return {
        'id': fahrplan.id,
        'name': fahrplan.name,
        'gueltig_von': fahrplan.gueltig_von.isoformat() if fahrplan.gueltig_von else None,
        'gueltig_bis': fahrplan.gueltig_bis.isoformat() if fahrplan.gueltig_bis else None,
        'fahrtdurchfuehrungen': [serialize_fahrtdurchfuehrung(fd) for fd in fahrplan.fahrtdurchfuehrungen]
    }


def serialize_fahrtdurchfuehrung(fahrtdurchfuehrung):
    return {
        'id': fahrtdurchfuehrung.id,
        'startZeit': fahrtdurchfuehrung.startZeit.isoformat() if fahrtdurchfuehrung.startZeit else None,
        'ausfall': fahrtdurchfuehrung.ausfall,
        'verspaetung': fahrtdurchfuehrung.verspaetung,
        'preis': fahrtdurchfuehrung.preis,
        'zug_id': fahrtdurchfuehrung.zug_id,
        'mitarbeiter': [serialize_mitarbeiter_durchfuehrung(md) for md in fahrtdurchfuehrung.mitarbeiter]
    }


def serialize_mitarbeiter_durchfuehrung(mitarbeiter_durchfuehrung):
    return {
        'mitarbeiter_id': mitarbeiter_durchfuehrung.mitarbeiter_id,
        'durchfuehrung_id': mitarbeiter_durchfuehrung.durchfuehrung_id
    }