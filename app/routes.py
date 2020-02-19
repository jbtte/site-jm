from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ParentInput
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Balance
from werkzeug.urls import url_parse

@app.route('/', methods = ["GET", "POST"])
@app.route('/index', methods = ["GET", "POST"])
@login_required
def index():
    balance = Balance.current_balance(user_id=2)
    account_statement = Balance.account_statement(user_id=2)
    form = ParentInput()

    if form.validate_on_submit():
        op = Balance(ammount=form.ammount.data, operation=int(form.operation.data), description=form.description.data, timestamp=form.timestamp.data , user_id=2)
        db.session.add(op)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', title='Home', balance=balance, account_statement=account_statement, form = form)

@app.route('/login', methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data, parent=form.is_parent.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
