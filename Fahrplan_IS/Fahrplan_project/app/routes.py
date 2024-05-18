from urllib.parse import urlsplit

import requests
from flask import render_template, flash, redirect, url_for, request, session

from app import app, database
from app.forms.halteplanCreateForm import HalteplanCreateForm, HalteplanChooseHaltepunktForm
from app.forms.halteplanEditForm import HalteplanEditForm
from app.forms.loginForm import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

from app.forms.mitarbeiterEditForm import MitarbeiterEditForm
from app.forms.mitarbeiterRegistrationForm import MitarbeiterRegistrationForm
from app.models.abschnitt import Abschnitt
from app.models.abschnitt_halteplan import AbschnittHalteplan
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

        flash('Erfolgreich neuen Halteplan erstellt')
        return redirect(url_for('halteplanList'))
    return render_template('chooseHaltestellen.html', title='Haltestellen auswählen', form=form)


@app.route('/editHalteplan/<int:id>', methods=['GET', 'POST'])
@login_required
def editHalteplan(id):
    halteplan = database.baseController.find_by_id(Halteplan, id)
    if halteplan is not None:
        form = HalteplanEditForm(request.form)
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



def formatAbschnittDTO_to_abschnitt(abschnittDTO):
    return {
        'spurenweite': abschnittDTO['maximale_spurweite'],
        'nutzungsentgelt': abschnittDTO['nutzungsentgelt'],
        'StartBahnhof': abschnittDTO['startbahnhof_id'],
        'EndBahnhof': abschnittDTO['endbahnhof_id']

    }