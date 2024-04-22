from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from app import db
from app.forms import RegistrationForm
from app.forms import BahnhofForm
from app.models import Bahnhof
from app.forms import AbschnittForm
from app.models import Abschnitt
from app.forms import WarnungForm
from app.models import Warnung
from app.forms import StreckeForm
from app.models import Strecke
from sqlalchemy.orm import joinedload
from datetime import date
from flask import jsonify

@app.route('/')
@app.route('/index')
@login_required
def index():
    bahnhof = Bahnhof.query.all()
    abschnitt = Abschnitt.query.options(joinedload(Abschnitt.startbahnhof), joinedload(Abschnitt.endbahnhof)).all()
    strecke = Strecke.query.all()
    warnungen = Warnung.query.options(joinedload(Warnung.abschnitt)).all()
    warnungen = [warnung for warnung in warnungen if warnung.gueltigkeitsdatum >= date.today()]

    for abschnitt_item in abschnitt:
        if any(warnung.abschnitt_id_warnung == abschnitt_item.abschnitt_id for warnung in warnungen):
            abschnitt_item.warnung = True
        else:
            abschnitt_item.warnung = False


    return render_template("index.html", title='Home Page',  bahnhof=bahnhof, strecke=strecke, abschnitt=abschnitt, warnungen=warnungen)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
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

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_role(form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/bahnhof', methods=['GET', 'POST'])
@login_required
def bahnhof():
    form = BahnhofForm()
    if form.validate_on_submit():
        bahnhof = Bahnhof(name=form.name.data, adresse=form.adresse.data, latitude=form.latitude.data, longitude=form.longitude.data)
        db.session.add(bahnhof)
        db.session.commit()
        flash('Der Bahnhof wurde erfolgreich hinzugefügt!')
        return redirect(url_for('bahnhof'))
    bahnhof = Bahnhof.query.all()
    return render_template('bahnhof.html', title='Bahnhof', bahnhof=bahnhof, form=form)

@app.route('/bahnhof/edit/<name>', methods=['GET', 'POST'])
@login_required
def edit_bahnhof(name):
    bahnhof = Bahnhof.query.get(name)
    if bahnhof is None:
        flash('Bahnhof {} existiert nicht.'.format(name))
        return redirect(url_for('bahnhof'))
    form = BahnhofForm(obj=bahnhof)
    if form.validate_on_submit():
        form.populate_obj(bahnhof)
        db.session.commit()
        flash('Die Änderungen wurden gespeichert.')
        return redirect(url_for('bahnhof'))
    return render_template('edit_bahnhof.html', form=form)

@app.route('/bahnhof/delete/<name>', methods=['POST'])
@login_required
def delete_bahnhof(name):
    bahnhof = Bahnhof.query.get(name)
    if bahnhof is None:
        flash('Bahnhof {} existiert nicht.'.format(name))
        return redirect(url_for('bahnhof'))
    db.session.delete(bahnhof)
    db.session.commit()
    flash('Der Bahnhof wurde gelöscht.')
    return redirect(url_for('bahnhof'))

@app.route('/abschnitt', methods=['GET', 'POST'])
@login_required
def abschnitt():
    form = AbschnittForm()
    if form.validate_on_submit():
        abschnitt = Abschnitt(startbahnhof_id=form.startbahnhof_id.data, endbahnhof_id=form.endbahnhof_id.data, maximale_geschwindigkeit=form.maximale_geschwindigkeit.data, maximale_spurweite=form.maximale_spurweite.data, nutzungsentgelt=form.nutzungsentgelt.data, distanz=form.distanz.data, strecke_id=form.strecke_id.data)
        strecke = Strecke.query.get_or_404(form.strecke_id.data)
        strecke.abschnitte.append(abschnitt)
        if strecke.validate_strecke() is None and form.strecke_validieren.data == True:
            flash(
                'Der Abschnitt konnte nicht hinzugefügt werden, da die Strecke {} nicht mehr zusammenhängend wäre oder es mehrdeutige Pfade gibt.'.format(
                    form.strecke_id.data))
            return redirect(url_for('abschnitt'))
        db.session.add(abschnitt)
        db.session.commit()
        flash('Der Abschnitt wurde erfolgreich hinzugefügt!')
        return redirect(url_for('abschnitt'))
    abschnitte = Abschnitt.query.all()
    return render_template('abschnitt.html', title='Abschnitt', abschnitte=abschnitte, form=form)

@app.route('/abschnitt/edit/<abschnitt_id>', methods=['GET', 'POST'])
@login_required
def edit_abschnitt(abschnitt_id):
    abschnitt = Abschnitt.query.get_or_404(abschnitt_id)
    form = AbschnittForm(obj=abschnitt)
    if form.validate_on_submit():
        form.populate_obj(abschnitt)
        db.session.commit()
        flash('Die Änderungen wurden gespeichert.')
        return redirect(url_for('abschnitt'))
    return render_template('edit_abschnitt.html', form=form)

@app.route('/abschnitt/delete/<abschnitt_id>', methods=['POST'])
@login_required
def delete_abschnitt(abschnitt_id):
    abschnitt = Abschnitt.query.get_or_404(abschnitt_id)
    db.session.delete(abschnitt)
    db.session.commit()
    flash('Der Abschnitt wurde erfolgreich gelöscht.')
    return redirect(url_for('abschnitt'))

@app.route('/warnungen', methods=['GET', 'POST'])
@login_required
def warnungen():
    form = WarnungForm()
    if form.validate_on_submit():
        warnung = Warnung(abschnitt_id_warnung=form.abschnitt_id_warnung.data, titel=form.titel.data, gueltigkeitsdatum=form.gueltigkeitsdatum.data, beschreibung=form.beschreibung.data)
        db.session.add(warnung)
        db.session.commit()
        flash('Warnung hinzugefügt')
        return redirect(url_for('warnungen'))
    warnungen = Warnung.query.options(joinedload(Warnung.abschnitt)).all()
    return render_template('warnungen.html', title='Warnungen', warnungen=warnungen, form=form)

@app.route('/warnung/edit/<int:warnung_id>', methods=['GET', 'POST'])
@login_required
def edit_warnung(warnung_id):
    warnung = Warnung.query.get_or_404(warnung_id)
    form = WarnungForm(obj=warnung)
    if form.validate_on_submit():
        form.populate_obj(warnung)
        db.session.commit()
        flash('Die Änderungen wurden gespeichert.')
        return redirect(url_for('warnungen'))
    return render_template('edit_warnung.html', form=form)

@app.route('/warnung/delete/<int:warnung_id>', methods=['POST'])
@login_required
def delete_warnung(warnung_id):
    warnung = Warnung.query.get_or_404(warnung_id)
    db.session.delete(warnung)
    db.session.commit()
    flash('Warnung gelöscht')
    return redirect(url_for('warnungen'))


@app.route('/strecke', methods=['GET', 'POST'])
@login_required
def strecke():
    form = StreckeForm()
    if form.validate_on_submit():
        strecke = Strecke(name=form.name.data)
        db.session.add(strecke)
        db.session.commit()
        flash('Die Strecke wurde erfolgreich erstellt.')
        return redirect(url_for('strecke'))
    strecken = Strecke.query.options(joinedload(Strecke.abschnitte)).all()
    for strecke in strecken:
        strecke.abschnitte = strecke.validate_strecke()
    return render_template('strecke.html', form=form, strecken=strecken)

@app.route('/strecke/delete/<name>', methods=['POST'])
@login_required
def delete_strecke(name):
    strecke = Strecke.query.get_or_404(name)
    db.session.delete(strecke)
    db.session.commit()
    flash('Die Strecke wurde erfolgreich gelöscht.')
    return redirect(url_for('strecke'))

@app.route('/api/warnung/<int:warnung_id>', methods=['GET'])
def get_warnung(warnung_id):
    warnung = Warnung.query.get(warnung_id)
    if warnung is None:
        return jsonify({'message': 'Warnung not found'}), 404
    return jsonify({'titel': warnung.titel, 'gueltigkeitsdatum': warnung.gueltigkeitsdatum})

@app.errorhandler(500)
def internal_error(error):
    flash('Server Error: Achten Sie darauf, dass der Eintrag nicht bereits existiert und versuchen Sie die Eingabe erneut!.')
    return redirect(url_for('index'))
