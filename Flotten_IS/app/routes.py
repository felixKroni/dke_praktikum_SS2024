from flask import render_template, flash
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from flask import request
from urllib.parse import urlsplit
from app.forms import LoginForm, TriebwagenForm, PersonenwagenForm, UpdateTriebwagenForm, UpdatePersonenwagenForm, ZugForm, UpdateZugForm, CreateUserForm, UpdateUserForm, WartungForm, UpdateWartungForm
from flask_login import logout_user
from flask_login import login_required
from flask import redirect, url_for
from flask import jsonify
from functools import wraps

from app.models import User, Wagen, Triebwagen, Personenwagen, Zug, Wartung



from app import app




def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Sie dürfen nicht auf diese Seite zugreifen!')
            return redirect(url_for('zugOverview'))
        return f(*args, **kwargs)
    return decorated_function


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
            next_page = url_for('zugOverview')
        return redirect(next_page)
    return render_template('login.html', title='homepage', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/createUser', methods=['GET', 'POST'])
@login_required
@admin_required
def createUser():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('userOverview'))
    return render_template('create_user.html', title='Create User', form=form)


@app.route('/userOverview')
@login_required
def userOverview():
    users = User.query.all()
    return render_template('useroverview.html', users=users)

@app.route('/updateUser/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def updateUser(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.id == user.id:
        flash('Sie können sich selbst nicht aktualisieren oder löschen.')
        return redirect(url_for('userOverview'))

    form = UpdateUserForm(obj=user)
    if form.validate_on_submit():
        new_username = form.username.data
        existing_user = User.query.filter(User.username == new_username).first()
        if existing_user and existing_user.id != user_id:
            flash('Benutzername existiert bereits. Bitte wählen Sie einen anderen!', 'error')
            return redirect(request.url)

        existing_user = User.query.filter(User.email == form.email.data).first()
        if existing_user and existing_user.id != user_id:
            flash('Email existiert bereits. Bitte wählen Sie einen anderen!', 'error')
            return redirect(request.url)

        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Änderungen wurden erfolgreich durchgeführt!')
        return redirect(url_for('userOverview'))
    return render_template('update_user.html', title='Update User', form=form)

@app.route('/deleteUser/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def deleteUser(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Sie können sich selbst nicht löschen.')
        return redirect(url_for('userOverview'))

    db.session.delete(user)
    db.session.commit()
    flash('User wurde erfolgreich gelöscht!')
    return redirect(url_for('userOverview'))


@app.route('/wagenOverview')
@login_required
def wagenOverview():
        triebwagen = Triebwagen.query.all()
        personenwagen = Personenwagen.query.all()
        # Get zug for personenwagen
        for p in personenwagen:
            p.zug = Zug.query.filter_by(zug_nummer=p.zug_nummer).first()

        return render_template('wagenoverview.html', title='Wagenübersicht', triebwagen=triebwagen, personenwagen=personenwagen)


@app.route('/Wagen_erstellen/<typ>', methods=['GET', 'POST'])
@login_required
@admin_required
def createWagen(typ):
    form = TriebwagenForm() if typ == 'Triebwagen' else PersonenwagenForm()

    if form.validate_on_submit():
        wagen_data = {
            'wagennummer': form.wagennummer.data,
            'spurweite': form.spurweite.data
        }
        if typ == 'Triebwagen':
            wagen_data['maxZugkraft'] = form.maxZugkraft.data
            wagen = Triebwagen(**wagen_data)
        else:
            wagen_data['sitzanzahl'] = form.sitzanzahl.data
            wagen_data['maximalgewicht'] = form.maximalgewicht.data
            wagen = Personenwagen(**wagen_data)

        db.session.add(wagen)
        db.session.commit()
        flash(typ + ' wurde erfolgreich erstellt!')
        return redirect(url_for('wagenOverview'))

    return render_template('create_wagen.html', title=typ + ' erstellen', wagenart=typ, form=form)


@app.route('/Wagen_bearbeiten/<wagennummer>', methods=['GET', 'POST'])
@login_required
@admin_required
def updateWagen(wagennummer):
    wagen = Wagen.query.filter_by(wagennummer=wagennummer).first()

    if wagen is None:
        flash('Es wurde kein Wagenn unter der Wagennummer {} gefunden!'.format(wagennummer))
        return redirect(url_for('wagenOverview'))

    typ = 'Triebwagen' if isinstance(wagen, Triebwagen) else 'Personenwagen'
    form = UpdateTriebwagenForm(wagennummer) if isinstance(wagen, Triebwagen) else UpdatePersonenwagenForm(wagennummer)

    if form.validate_on_submit():
        wagen.wagennummer = form.wagennummer.data
        wagen.spurweite = form.spurweite.data

        if isinstance(wagen, Triebwagen):
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
        if isinstance(wagen, Triebwagen):
            form.maxZugkraft.data = wagen.maxZugkraft
        else:
            form.sitzanzahl.data = wagen.sitzanzahl
            form.maximalgewicht.data = wagen.maximalgewicht

    return render_template('update_wagen.html', title='Wagen update', wagenart=typ, form=form)


@app.route('/Wagen_löschen/<wagennummer>', methods=['POST'])
@login_required
@admin_required
def deleteWagen(wagennummer):
    wagen = Wagen.query.filter_by(wagennummer=wagennummer).first()

    if not wagen:
        flash('Wagen nicht gefunden!', 'error')
        return redirect(url_for('wagenOverview'))

    if isinstance(wagen, Triebwagen):
        zug = Zug.query.filter_by(triebwagen_nr=wagennummer).first()
        if zug:
            flash('Warnung! Triebwagen {} wird in einem Zug verwendet und kann nicht gelöscht werden!'.format(wagennummer), 'error')
            return redirect(url_for('wagenOverview'))

    if isinstance(wagen, Personenwagen):
        zug = Zug.query.filter(Zug.personenwagen.any(wagennummer=wagennummer)).first()
        if zug:
            flash('Warnung! Personenwagen {} wird in einem Zug verwendet und kann nicht gelöscht werden!'.format(wagennummer), 'error')
            return redirect(url_for('wagenOverview'))

    db.session.delete(wagen)
    db.session.commit()
    flash('{} wurde erfolgreich gelöscht!'.format(wagennummer))
    return redirect(url_for('wagenOverview'))


@app.route('/')
@app.route('/Zugübersicht')
@login_required
def zugOverview():
    zug = Zug.query.order_by('zug_name').all()
    return render_template('zugoverview.html', title='Zugübersicht', zug=zug)



@app.route('/Zug_erstellen', methods=['GET', 'POST'])
@login_required
@admin_required
def createZug():
    triebwagen = Triebwagen.query.all()
    personenwagen = Personenwagen.query.all()
    form = ZugForm()

    form.triebwagen_nr.choices = [(t.wagennummer, str(t.wagennummer) + " (" + str(t.spurweite) + " mm - " + str(t.maxZugkraft) + " Tonnen)" ) for t in Triebwagen.query.filter_by(zug=None)]

    if form.validate_on_submit():
        if not form.triebwagen_nr.data:
            flash('Bitte wählen Sie einen Triebwagen aus!')
            return redirect(url_for('createZug'))

        personenwagenListe = request.form.getlist('List_PW')
        if personenwagenListe == []:
            flash('Bitte wählen Sie einen Personenwagen aus!')
            return redirect(url_for('createZug'))

        wagen = []
        for liste in personenwagenListe:
            w = Personenwagen.query.filter_by(wagennummer=liste).first()

            if w.zug is not None:
                flash('Der Personenwagen wurde bereits verwendet!'.format(w.wagennummer))
                return redirect(url_for('createZug'))

            wagen.append(w)

        total_weight = sum(w.maximalgewicht for w in wagen)
        triebwagen = Triebwagen.query.filter_by(wagennummer=form.triebwagen_nr.data).first()

        if total_weight > triebwagen.maxZugkraft:
            flash('Warnung! Der Triebwagen hat nicht genug Zugkraft, um alle Personenwagen zu ziehen!')
            return redirect(url_for('createZug'))

        spurweite = Triebwagen.query.filter_by(wagennummer=form.triebwagen_nr.data).first().spurweite
        for w in wagen:
            if spurweite != w.spurweite:
                flash('Warnung! Wagen müssen gleiche Spurweite haben!')
                return redirect(url_for('createZug'))

        zug = Zug(zug_nummer=form.zug_nummer.data, zug_name=form.zug_name.data, triebwagen_nr=form.triebwagen_nr.data, personenwagen=wagen)
        db.session.add(zug)
        db.session.commit()
        flash('Zug wurde erfolgreich erstellt!')
        return redirect(url_for('zugOverview'))

    return render_template('create_zug.html', title='Zug erstellen', triebwagen=triebwagen, personenwagen=personenwagen, form=form)

@app.route('/Zug_bearbeiten/<zug_nummer>', methods=['GET', 'POST'])
@login_required
@admin_required
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

    form.triebwagen_nr.choices = [(t.wagennummer, str(t.wagennummer) + " (" + str(t.spurweite) + " mm - " + str(t.maxZugkraft) + " Tonnen)" ) for t in
                                  aktZug]

    if form.validate_on_submit():
        if not form.triebwagen_nr.data:
            flash('Bitte wählen Sie einen Triebwagen aus!')
            return redirect(url_for('createZug'))

        personenwagenListe = request.form.getlist('List_PW')
        if personenwagenListe == []:
            flash('Bitte wählen Sie einen Personenwagen aus!')
            return redirect(url_for('updateZug', zug_nummer=zug_nummer))

        wagen = []
        for liste in personenwagenListe:
            w = Personenwagen.query.filter_by(wagennummer=liste).first()

            if w.zug is not None and w.zug_nummer != zug.zug_nummer:
                flash('Der Personenwagen {} ist bereits einem Zug zugeordnet!'.format(
                    w.zug_nummer))
                return redirect(url_for('updateZug', zug_nummer=zug_nummer))
            wagen.append(w)

        total_weight = sum(w.maximalgewicht for w in wagen)
        triebwagen = Triebwagen.query.filter_by(wagennummer=form.triebwagen_nr.data).first()

        if total_weight > triebwagen.maxZugkraft:
            flash('Warnung! Der Triebwagen hat nicht genug Zugkraft, um alle Personenwagen zu ziehen!')
            return redirect(url_for('updateZug', zug_nummer=zug_nummer))

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
@admin_required
def deleteZug(zug_nummer):
    zug = Zug.query.filter_by(zug_nummer=zug_nummer).first()

    if zug is None:
        flash('Zug mit der Nummer {} nicht gefunden!'.format(zug_nummer), 'error')
        return redirect(url_for('zugOverview'))

    wartung = Wartung.query.filter_by(zug_nummer=zug_nummer).first()
    if wartung:
        flash('Zug {} wird in einer Wartung verwendet und kann nicht gelöscht werden!'.format(zug_nummer), 'error')
        return redirect(url_for('zugOverview'))

    db.session.delete(zug)
    db.session.commit()
    flash('Zug {} wurde erfolgreich gelöscht!'.format(zug_nummer))
    return redirect(url_for('zugOverview'))



@app.route('/api/züge', methods=['GET'])
def get_zug():
    zug = Zug.query.outerjoin(Wartung).filter(
        (Wartung.zug_nummer == None) | (Wartung.end_time < sa.func.now())
    ).all()

    if not zug:
        return jsonify({'message': 'Keine verfügbaren Züge'}), 404

    zug_data = []
    for z in zug:
        zug_data.append({
            'zug_nummer': z.zug_nummer,
            'zug_name': z.zug_name,
            'triebwagen_nr': z.triebwagen_nr,
            'personenwagen': [pw.wagennummer for pw in z.personenwagen],
            'spurweite': z.triebwagen.spurweite
        })
    return jsonify(zug_data)



@app.route('/wartungOverview')
@login_required
def wartungOverview():
    if current_user.is_admin:
        wartungen = Wartung.query.all()
    else:
        user_id = current_user.id
        wartungen = Wartung.query.join(Wartung.mitarbeiters).filter(User.id == user_id).all()

    return render_template('wartungoverview.html', wartungen=wartungen)


@app.route('/createWartung', methods=['GET', 'POST'])
@login_required
@admin_required
def createWartung():
    form = WartungForm()
    form.mitarbeiter_ids.choices = [(u.id, u.username) for u in User.query.filter_by(is_admin=False).all()]
    form.zug_nummer.choices = [(z.zug_nummer, z.zug_name) for z in Zug.query.all()]

    if form.validate_on_submit():
        mitarbeiter_ids = form.mitarbeiter_ids.raw_data
        start_time = form.start_time.data
        end_time = form.end_time.data

        for mitarbeiter_id in mitarbeiter_ids:
            mitarbeiter = User.query.get(mitarbeiter_id)
            for wartung in mitarbeiter.wartungs:
                if wartung.wartung_nr == form.wartung_nr.data:
                    continue

                if (
                    (wartung.start_time <= start_time <= wartung.end_time)
                    or (wartung.start_time <= end_time <= wartung.end_time)
                    or (start_time <= wartung.start_time <= end_time)
                    or (start_time <= wartung.end_time <= end_time)
                ):
                    flash('Warning: Mitarbeiter {mitarbeiter.username} ist von {start_time} bis {end_time} nicht verfügbar!!')
                    return redirect(url_for('createWartung'))

        wartung = Wartung(
            wartung_nr = form.wartung_nr.data,
            zug_nummer=form.zug_nummer.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(wartung)
        db.session.commit()

        for mitarbeiter_id in mitarbeiter_ids:
            wartung.mitarbeiters.append(User.query.get(mitarbeiter_id))

        db.session.commit()

        flash('Wartung wurde erfolgreich erstellt!')
        return redirect(url_for('wartungOverview'))

    return render_template('create_wartung.html', form=form)


@app.route('/updateWartung/<wartung_nr>', methods=['GET', 'POST'])
@login_required
@admin_required
def updateWartung(wartung_nr):
    wartung = Wartung.query.filter_by(wartung_nr=wartung_nr).first()
    if wartung is None:
        flash('Wartung nicht gefunden!')
        return redirect(url_for('wartungOverview'))

    mitarbeiter_ids = [m.id for m in wartung.mitarbeiters]

    form = UpdateWartungForm(
        original_wartung_nr=wartung.wartung_nr,
        original_mitarbeiter_ids=mitarbeiter_ids,
        original_zug_nummer=wartung.zug_nummer,
        original_start_time=wartung.start_time,
        original_end_time=wartung.end_time,
        obj=wartung
    )

    form.mitarbeiter_ids.choices = [(u.id, u.username, True if u.id in mitarbeiter_ids else False) for u in User.query.filter_by(is_admin=False).all()]
    form.zug_nummer.choices = [(z.zug_nummer, z.zug_name) for z in Zug.query.all()]

    if form.validate_on_submit():
        form_mitarbeiter_ids = form.mitarbeiter_ids.raw_data
        start_time = form.start_time.data
        end_time = form.end_time.data


        for mitarbeiter_id in form_mitarbeiter_ids:
            mitarbeiter = User.query.get(mitarbeiter_id)
            for wartung in mitarbeiter.wartungs:
                if wartung.wartung_nr == form.wartung_nr.data:
                    continue

                if (
                    (wartung.start_time <= start_time <= wartung.end_time)
                    or (wartung.start_time <= end_time <= wartung.end_time)
                    or (start_time <= wartung.start_time <= end_time)
                    or (start_time <= wartung.end_time <= end_time)
                ):

                    flash('Warning: Mitarbeiter {mitarbeiter.username} ist von {start_time} bis {end_time} nicht verfügbar!')

                    return redirect(url_for('updateWartung' ,wartung_nr=wartung_nr))

        wartung.wartung_nr = form.wartung_nr.data
        wartung.zug_nummer = form.zug_nummer.data
        wartung.start_time = start_time
        wartung.end_time = end_time
        db.session.commit()

        wartung.mitarbeiters.clear()
        db.session.commit()

        for mitarbeiter_id in form.mitarbeiter_ids.raw_data:
            wartung.mitarbeiters.append(User.query.get(mitarbeiter_id))
        db.session.commit()

        flash('Wartung wurde erfolgreich aktualisiert!')
        return redirect(url_for('wartungOverview'))

    return render_template('update_wartung.html', form=form, wartung=wartung)



@app.route('/deleteWartung/<wartung_nr>', methods=['POST'])
@login_required
@admin_required
def deleteWartung(wartung_nr):
    wartung = Wartung.query.filter_by(wartung_nr=wartung_nr).first()
    if wartung is None:
        flash('Wartung nicht gefunden!')
        return redirect(url_for('wartungOverview'))

    db.session.delete(wartung)
    db.session.commit()
    flash('Wartung wurde erfolgreich gelöscht!')
    return redirect(url_for('wartungOverview'))


