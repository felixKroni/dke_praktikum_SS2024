from flask import render_template, flash
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from flask import request
from urllib.parse import urlsplit
from app.forms import LoginForm, RegistrationForm, TriebwagenForm, PersonenwagenForm, UpdateTriebwagenForm, UpdatePersonenwagenForm, ZugForm, UpdateZugForm
from flask_login import logout_user
from flask_login import login_required
from flask import redirect, url_for
from flask import jsonify

from app.models import User, Wagen, Triebwagen, Personenwagen, Zug



from app import app

@app.route('/')
@app.route('/index')
@login_required
def index():
    zug = Zug.query.order_by('zug_name').all()
    return render_template('zugoverview.html', title='Home', zug=zug)

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
    return render_template('login.html', title='homepage', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/wagenOverview')
@login_required
def wagenOverview():
    triebwagen = Triebwagen.query.all()
    personenwagen = Personenwagen.query.all()
    return render_template('wagenoverview.html', title='Wagenübersicht', triebwagen=triebwagen, personenwagen=personenwagen)



@app.route('/Wagen_erstellen/<typ>', methods=['GET', 'POST'])
@login_required
def createWagen(typ):
    global wagen
    if typ == 'Triebwagen':
        form = TriebwagenForm()
    else:
        form = PersonenwagenForm()

    if form.validate_on_submit():
        if typ == 'Triebwagen':
            wagen = Triebwagen(wagennummer=form.wagennummer.data, spurweite=form.spurweite.data, maxZugkraft=form.maxZugkraft.data)
        elif typ == 'Personenwagen':
            wagen = Personenwagen(wagennummer=form.wagennummer.data, spurweite=form.spurweite.data, sitzanzahl=form.sitzanzahl.data,
                                  maximalgewicht=form.maximalgewicht.data)
        db.session.add(wagen)
        db.session.commit()
        flash(typ + ' wurde erfolgreich erstellt!')
        return redirect(url_for('wagenOverview'))

    return render_template('create_wagen.html', title=typ + ' erstellen', wagenart=typ, form=form)

@app.route('/Wagen_bearbeiten/<wagennummer>', methods=['GET', 'POST'])
@login_required
def updateWagen(wagennummer):
    wagen = Wagen.query.filter_by(wagennummer=wagennummer).first()

    if wagen is None:
        flash('Es wurde kein Waggon unter der Wagennummer {} gefunden!'.format(wagennummer))
        return redirect(url_for('wagenOverview'))

    elif type(wagen) == Triebwagen:
        typ = 'Triebwagen'
        form = UpdateTriebwagenForm(wagen.wagennummer)
    else:
        typ = 'Personenwagen'
        form = UpdatePersonenwagenForm(wagen.wagennummer)

    if form.validate_on_submit():
        wagen.wagennummer = form.wagennummer.data
        wagen.spurweite = form.spurweite.data

        if type(wagen) == Triebwagen:
            wagen.maxZugkraft = form.maxZugkraft.data
        else:
            wagen.sitzanzahl = form.sitzanzahl.data
            wagen.maximalgewicht = form.maximalgewicht.data

        db.session.commit()
        flash('Änderungen wurden erfolgreich durchgeführt!')
        return redirect(url_for('wagenOverview'))

    elif request.method == 'GET':
        form.wagennummer.data = wagen.wagennummer
        form.spurweite.data = wagen.spurweite
        if type(wagen) == Triebwagen:
            form.maxZugkraft.data = wagen.maxZugkraft
        else:
            form.sitzanzahl.data = wagen.sitzanzahl
            form.maximalgewicht.data = wagen.maximalgewicht

    return render_template('update_wagen.html', title='Wagen update', wagenart=typ, form=form)

@app.route('/Wagen_löschen/<wagennummer>', methods=['POST'])
@login_required
def deleteWagen(wagennummer):
    wagen = Wagen.query.filter_by(wagennummer=wagennummer).first()
    db.session.delete(wagen)
    if type(wagen) == Personenwagen:
            zug = Zug.query.filter_by(zug_nummer=wagen.zug_nummer).first()
            if zug is not None and zug.personenwagen.first() is None:
                db.session.delete(zug)

    db.session.commit()
    flash('Wagen mit der Wagennummer {} wurde erfolgreich gelöscht!'.format(wagennummer))
    return redirect(url_for('wagenOverview'))

@app.route('/Zugübersicht')
@login_required
def zugOverview():
    zug = Zug.query.order_by('zug_name').all()
    return render_template('zugoverview.html', title='Zugübersicht', zug=zug)



@app.route('/Zug_erstellen', methods=['GET', 'POST'])
@login_required
def createZug():
    triebwagen = Triebwagen.query.all()
    personenwagen = Personenwagen.query.all()
    form = ZugForm()

    form.triebwagen_nr.choices = [(t.wagennummer, str(t.wagennummer) + " (" + str(t.spurweite) + " mm)") for t in Triebwagen.query.filter_by(zug=None)]

    if form.validate_on_submit():
        personenwagenListe = request.form.getlist('personenwagenCheckbox')
        if personenwagenListe == []:
            flash('Fehler: Ein Zug benötigt mindestens einen Personenwagen!')
            return redirect(url_for('createZug'))

        wagen = []
        for liste in personenwagenListe:
            w = Personenwagen.query.filter_by(wagennummer=liste).first()

            if w.zug is not None:
                flash('Fehler: Der Personenwagen wurde bereits verwendet!'.format(w.wagennummer))
                return redirect(url_for('createZug'))

            wagen.append(w)

        spurweite = Triebwagen.query.filter_by(wagennummer=form.triebwagen_nr.data).first().spurweite
        for w in wagen:
            if spurweite != w.spurweite:
                flash('Wagen müssen gleiche Spurweite haben!')
                return redirect(url_for('createZug'))

        zug = Zug(zug_nummer=form.zug_nummer.data, zug_name=form.zug_name.data, triebwagen_nr=form.triebwagen_nr.data, personenwagen=wagen)
        db.session.add(zug)
        db.session.commit()
        flash('Zug wurde erfolgreich erstellt!')
        return redirect(url_for('zugOverview'))

    return render_template('create_zug.html', title='Zug erstellen', triebwagen=triebwagen, personenwagen=personenwagen, form=form)

@app.route('/Zug_bearbeiten/<zug_nummer>', methods=['GET', 'POST'])
@login_required
def updateZug(zug_nummer):
    zug = Zug.query.filter_by(zug_nummer=zug_nummer).first()
    if zug is None:
        flash('Es wurde kein Zug unter der Zugnummer {} gefunden!'.format(zug_nummer))
        return redirect(url_for('zugOverview'))

    personenwagen = Personenwagen.query.all()
    form = UpdateZugForm(zug.zug_nummer, zug.triebwagen_nr)
    aktZug = list(Triebwagen.query.filter_by(zug=zug))

    for t in Triebwagen.query.filter_by(zug=None):
        aktZug.append(t)

    form.triebwagen_nr.choices = [(t.wagennummer, str(t.wagennummer) + " (" + str(t.spurweite) + " mm)") for t in
                                  aktZug]

    if form.validate_on_submit():
        personenwagenListe = request.form.getlist('personenwagenCheckbox')
        if personenwagenListe == []:
            flash('Fehler: Ein Zug benötigt mindestens einen Personenwagen!')
            return redirect(url_for('updateZug', zug_nummer=zug_nummer))

        wagen = []
        for liste in personenwagenListe:
            w = Personenwagen.query.filter_by(wagennummer=liste).first()

            if w.zug is not None and w.zug_nummer != zug.zug_nummer:
                flash('Fehler: Der Personenwagen mit der Wagennummer {} ist bereits einem Zug zugeordnet!'.format(
                    w.zug_nummer))
                return redirect(url_for('updateZug', zug_nummer=zug_nummer))
            wagen.append(w)

        spurweite = Triebwagen.query.filter_by(wagennummer=form.triebwagen_nr.data).first().spurweite
        for w in wagen:
            if spurweite != w.spurweite:
                flash('Wagen müssen gleiche Spurweite haben!')
                return redirect(url_for('updateZug', zug_nummer=zug_nummer))

        zug.zug_nummer = form.zug_nummer.data
        zug.zug_name = form.zug_name.data
        zug.triebwagen_nr = form.triebwagen_nr.data
        zug.personenwagen = wagen
        db.session.commit()
        flash('Änderungen wurden erfolgreich durchgeführt!')
        return redirect(url_for('zugOverview'))

    elif request.method == 'GET':
        form.zug_nummer.data = zug.zug_nummer
        form.zug_name.data = zug.zug_name
        form.triebwagen_nr.data = zug.triebwagen_nr

    return render_template('update_zug.html', title='Zug bearbeiten', zug=zug, personenwagen=personenwagen, form=form)


@app.route('/Zug_löschen/<zug_nummer>', methods=['POST'])
@login_required
def deleteZug(zug_nummer):

    zug = Zug.query.filter_by(zug_nummer=zug_nummer).first()
    if zug is None:
        return redirect(url_for('zugOverview'))
    db.session.delete(zug)
    db.session.commit()

    flash('Löschen des Zuges mit der Zugnummer {} wurde erfolgreich durchgeführt'.format(zug_nummer))
    return redirect(url_for('zugOverview'))

@app.route('/api/züge', methods=['GET'])
def get_zug():
    zug = Zug.query.all()
    if zug is None:
        return jsonify({'message': 'Der Zug ist nicht verfügbar'}), 404
    zug_data = []
    for z in zug:
        zug_data.append({
            'zug_nummer': z.zug_nummer,
            'zug_name': z.zug_name,
            'triebwagen_nr': z.triebwagen_nr,
            'personenwagen': [pw.wagennummer for pw in zug.personenwagen]
        })
    return jsonify(zug_data)
