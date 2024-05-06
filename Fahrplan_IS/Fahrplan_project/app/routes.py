from urllib.parse import urlsplit

from flask import render_template, flash, redirect, url_for, request

from app import app, database
from app.forms.loginForm import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

from app.forms.mitarbeiterRegistrationForm import MitarbeiterRegistrationForm
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = MitarbeiterRegistrationForm()
    if form.validate_on_submit():
        user = Mitarbeiter(username=form.username.data, email=form.email.data, svnr=form.svnr.data, name=form.name.data, role=form.role.data)
        user.set_password(form.password.data)
        database.baseController.add(user)
        #database.Session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registerMitarbeiter.html', title='Register', form=form)


@app.route('/mitarbeiterList', methods=['GET'])
@login_required
def mitarbeiterList():
    if current_user.is_authenticated:
        return render_template('mitarbeiterList.html', title='Mitarbeiter', mitarbeiters=database.baseController.find_all(Mitarbeiter))
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
            form = MitarbeiterRegistrationForm()
            form.username.data = user.username
            form.email.data = user.email
            form.svnr.data = user.svnr
            form.name.data = user.name
            form.role.data = user.role
            form.submit.label.text = 'Update'
            if form.validate_on_submit():
                user.username = form.username.data
                user.email = form.email.data
                user.svnr = form.svnr.data
                user.name = form.name.data
                user.role = form.role.data
                user.set_password(form.password.data)
                database.baseController.update()
                flash('Mitarbeiter updated')
                return redirect(url_for('mitarbeiterList'))
            return render_template('editMitarbeiter.html', title='Edit', form=form)
        return redirect(url_for('mitarbeiterList'))
    return redirect(url_for('index'))