from urllib.parse import urlsplit

from flask import render_template, flash, redirect, url_for, request

from app import app, database
from app.forms.halteplanCreateForm import HalteplanCreateForm
from app.forms.halteplanEditForm import HalteplanEditForm
from app.forms.loginForm import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

from app.forms.mitarbeiterEditForm import MitarbeiterEditForm
from app.forms.mitarbeiterRegistrationForm import MitarbeiterRegistrationForm
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
            flash('Invalid username or password')
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
        flash('Congratulations, you registered user: ' + user.username)
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
            flash('Mitarbeiter deleted')
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
                    flash('Mitarbeiter updated')
                return redirect(url_for('mitarbeiterList'))

            return render_template('editMitarbeiter.html', title='Edit', form=form)
        else:
            flash('No user found with id ' + id)
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
    if request.form is None:
        form = HalteplanCreateForm()
        strecken_list = [('strecke1', 'Orient Express Route'), ('strecke2', 'Westbahn')] #TODO get from strecken system
        form.streckenName.choices = strecken_list
        return render_template('createHalteplan.html', title='Create Halteplan', form=form)

    form = request.form
    if form.validate_on_submit():
        new_halteplan = Halteplan(name=form.name.data, streckenName=form.streckenName.data)
        database.baseController.add(new_halteplan)
        flash('New Halteplan created successfully')
        return redirect(url_for('halteplanList'))
    return render_template('createHalteplan.html', title='Create Halteplan', form=form)


@app.route('/editHalteplan/<int:id>', methods=['GET', 'POST'])
@login_required
def editHalteplan(id):
    halteplan = database.baseController.find_by_id(Halteplan, id)
    if halteplan is not None:
        form = HalteplanEditForm(request.form)
        if request.method == 'GET':
            form.name.data = halteplan.name
            form.streckenName.data = halteplan.streckenName
        elif form.validate_on_submit():
            halteplan.name = form.name.data
            halteplan.streckenName = form.streckenName.data
            database.baseController.update_by_id(Halteplan, id, halteplan.__dict__)
            flash('Halteplan updated successfully')
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
        database.baseController.delete_multiple(halteplan.abschnitte)
        database.baseController.delete(halteplan)
        flash('Halteplan deleted')
    else:
        flash('No Halteplan found with ID: {}'.format(id))
    return redirect(url_for('halteplanList'))
