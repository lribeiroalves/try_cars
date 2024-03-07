from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import SystemRandom
from flask_mail import Message
from flask_login import login_user, logout_user, current_user
import datetime

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from trycars.ext.mail_client.mail_client import mail
from .forms import RegisterForm, EmailConfirmationForm, LoginForm
from .token import generate_confirmation_token, confirm_token

def send_confirmation_email(token:str, recipients:list, first_link:bool=True) -> None:
    if first_link:
        greet_message = 'You have registered your TryCars account succesfully.'
    else:
        greet_message = 'This is a new confirmation code for your TryCars account.'

    confirmation_message = Message(
        subject='TryCars - Email Confirmation',
        recipients=recipients,
        html = f"""
        <p>
            {greet_message}
        </p>
        <p>
            Copy the link
            <p><strong>localhost:5000/auth/confirm/{token}</strong></p>
            and paste it into your browser to confirm your email and have access to all functionallity of the website.
        </p>
        <p>
            Thank You.
        </p>
        """
    )
    mail.send(message=confirmation_message)

def register_views(bp, app):
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form_register = RegisterForm()

        if form_register.validate_on_submit():
            # generate unique fs_uniquifier
            while True:
                fs = str(SystemRandom().getrandbits(64))[0:15]
                if db.session.execute(db.select(User).filter_by(fs_uniquifier=fs)).scalar() is None:
                    break

            user_role = db.session.execute(db.select(Role).filter_by(name='user')).scalar()
            if user_role is None:
                user_role = Role(name = 'user', description='Simple User')
            new_user = User(email=form_register.email.data, username=form_register.username.data, active=False, fs_uniquifier=fs, password=generate_password_hash(form_register.password.data), roles=user_role)
            db.session.add(new_user)
            db.session.commit()

            # email confirmation
            token = generate_confirmation_token(app, form_register.email.data)
            try:
                send_confirmation_email(token, [form_register.email.data])
            except:
                flash('Confirmation link has not been sent. Try again.')
                return render_template('auth/email_confirmation.html', confirmed = 'n', form=form_register)

            flash('User Registered Succesfully, check your email for your confirmation link.')
            return redirect(url_for('homepage.index'))

        return render_template('auth/register.html', form=form_register)


    @bp.route('/confirm/<token>')
    def confirmation(token):
        form = EmailConfirmationForm()
        email = confirm_token(app, token)

        if email is None:
            return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)
        else:
            user = db.session.execute(db.select(User).filter_by(email=email)).scalar()
            if user is None:
                return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)
            else:
                if user.active:
                    return render_template('auth/email_confirmation.html', confirmed = 'a', form=form)
                else:
                    user.active = True
                    user.confirmed_at = datetime.datetime.now()
                    db.session.commit()
                    flash('Your account is now active.')
                    return redirect(url_for('auth.login'))


    @bp.route('/confirmation/send', methods=['GET', 'POST'])
    def send_new_confirmation_link():
        form = EmailConfirmationForm()

        if form.validate_on_submit():
            # email confirmation
            token = generate_confirmation_token(app, form.email.data)
            try:
                send_confirmation_email(token, [form.email.data], False)
                flash('Confirmation link sent. Check your e-mail')
            except:
                flash('The confirmation link could not be sent. Try Again!')
                return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)

            return redirect(url_for('homepage.index'))
        
        else:
            return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)


    @bp.route('/logout', methods=['GET', 'POST'])
    def logout():
        return 'logout'
    

    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        """This view condensate the login and registration forms on a single page"""

        # login
        form_login = LoginForm()
        if form_login.validate_on_submit():
            user = db.session.execute(db.select(User).filter_by(username=form_login.login.data)).scalar()
            if user is not None and check_password_hash(user.password, form_login.password.data):
                login_user(user)
            else:
                return str(check_password_hash(user.password, form_login.password.data))

        # -----------------------------------------------------------------------------------------------
            
        # registration
        form_register = RegisterForm()
        if form_register.validate_on_submit():
            # generate unique fs_uniquifier
            while True:
                fs = str(SystemRandom().getrandbits(64))[0:15]
                if db.session.execute(db.select(User).filter_by(fs_uniquifier=fs)).scalar() is None:
                    break

            user_role = db.session.execute(db.select(Role).filter_by(name='user')).scalar()
            if user_role is None:
                user_role = Role(name = 'user', description='Simple User')
            new_user = User(email=form_register.email.data, username=form_register.username.data, active=False, fs_uniquifier=fs, password=generate_password_hash(form_register.password.data), roles=user_role)
            db.session.add(new_user)
            db.session.commit()

            # email confirmation
            token = generate_confirmation_token(app, form_register.email.data)
            try:
                send_confirmation_email(token, [form_register.email.data])
            except:
                flash('Confirmation link has not been sent. Try again.')
                return render_template('auth/email_confirmation.html', confirmed = 'n', form=form_register)

            flash('User Registered Succesfully, check your email for your confirmation link.')
            return redirect(url_for('homepage.index'))

        return render_template('auth/authentication.html', form_login=form_login, form_register=form_register)
    
