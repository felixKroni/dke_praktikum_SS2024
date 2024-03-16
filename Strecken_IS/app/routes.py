from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from app import db
from app.forms import RegistrationForm
from app.forms import BahnhofForm
from app.models import Bahnhof

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)

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
def delete_bahnhof(name):
    bahnhof = Bahnhof.query.get(name)
    if bahnhof is None:
        flash('Bahnhof {} existiert nicht.'.format(name))
        return redirect(url_for('bahnhof'))
    db.session.delete(bahnhof)
    db.session.commit()
    flash('Der Bahnhof wurde gelöscht.')
    return redirect(url_for('bahnhof'))